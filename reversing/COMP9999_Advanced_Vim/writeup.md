# COMP9999: Advanced Vim

## Authors

- Jarrod Cameron

## Category

- Reverse Engineering

## Description

SkyLang is a new programming language I invented. It's so new it can only be
run with my emulator. I don't want you to reverse engineer my code so I wrote
my emulator in the most obscure language I know!

The flag is in the format `SKYLIGHT{...}`

## Difficulty

- Child's Play

## Points

420

## Files

- sky.vim: The emulator which executes `vuln.sky`
- vuln.sky: A program compiled from SkyLang. Requires `sky.vim` to be run.

## Solution

<details>
<summary>Spoiler</summary>

### Idea

By modifying the emulator, it's possible to get a better idea of what
`vuln.sky` is doing. The code is decrypting the flag using XOR. The key to
decrypt the flag is five bytes long.

Once the encrypted flag is extracted, it's possible to perform a known plain
text attack to extract the flag.

### Walkthrough

#### 1. Checking Out The Files

Looking at vuln.sky there seems to be some hex encoded data. Just by looking
at the contents of the file there doesn't seem to be anything interesting.

```bash
$ cat vuln.sky
9235923692379238923a9231922e9230922e9230922e923792329231920e9202...
```

Looking at sky.vim shows a rather large Vim Script file. Despite there being
almost 300 lines of code it's important not to be intimidated.

```bash
$ cat sky.vim
" Welcome to my Emulator! VimScript is super easy and intuitive to understand!
"
" There is no input validation so be careful :D
"
" To use this file, run the command:
"         vim -S sky.vim path/to/prog.sky

function! LogInit()
        call writefile([''], 'sky.log', 'b')
endfunction

[snip]
```

From skimming through the code it's possible to make some observations:
- `SkyEmulator()` is the entry point. This can be seen by the `call
   SkyEmulator()` line at the bottom of the file.
- `SkyEmulator()` uses a dictionary to keep the state of the machine. For
  example, the `state` contains: `pc` (program counter), `sp` (stack pointer),
  `as` (address space), `text` (code), and `finish`.
- There are six system calls: `Exit()`, `Log()`, `Connect()`, `Read()`,
  `Send()`, and `Close()`. This can be seen from the `EmuSyscall()` function.

NOTE: Even if you don't know anything about Vim Script it's still possible to
make educated guesses about what the code is doing with your knowledge of other
programming languages.

#### 2. Executing vuln.sky

The sky.vim file says:

> To use this file, run the command:
>         vim -S sky.vim path/to/prog.sky

So if we run `vim -S sky.vim vuln.sky` we should be able to execute the file.
After running the command nothing interesting seems to happen. After exiting
vim there's a `sky.log` file however it's empty.

#### 3. Tracing System Calls

If you've ever taken an operating systems course, you probably know "syscalls"
(or "system calls") are the primary method a process can communicate with the
outside world. Without system calls, a process would be mostly limited to
reading memory and writing to memory in it's own address space.

If we can figure out what system calls are being called it might reveal
something about the internal workings of vuln.sky. But how should we print this
information? We aren't Vim Script experts so we probably don't know the easiest
way to get information from the emulator. However, two functions stick out:
`LogInit()` and `LogLine()`. By the names of these functions we can deduce they
probably involve manipulating a log file. The `LogLine()` function is probably
used to write to the log file (since it calls `writefile()` which probably...
writes to a file).

Each of the system calls can be edited to log when they are called. At the
start of some of the system calls it seems they _pop_ some data. It's possible
this is the way arguments are passed to the system calls so we might as well
log that as well.

```vim
function! EmuSyscallExit(state)
        call LogLine('Exit()')
        [snip]

function! EmuSyscallLog(state)
        let length = EmuPop(a:state)
        let addr = EmuPop(a:state)
        call LogLine('Log(addr='.addr.', length='.length.')')
        [snip]

function! EmuSyscallConnect(state)
        let length = EmuPop(a:state)
        let path = EmuPopStr(a:state, length)
        call LogLine('Connect(length='.length.', path='.path.')')
        [snip]

function! EmuSyscallRead(state)
        let addr = EmuPop(a:state)
        let length = EmuPop(a:state)
        let buf = EmuPop(a:state)
        call LogLine('Read(length='.length.', addr='.addr.', buf='.buf.')')
        [snip]

function! EmuSyscallSend(state)
        let addr = EmuPop(a:state)
        let length = EmuPop(a:state)
        let data = EmuPopStr(a:state, length)
        call LogLine('Read(length='.length.', addr='.addr.', data='.data.')')
        [snip]

function! EmuSyscallClose(state)
        let addr = EmuPop(a:state)
        call LogLine('Close(addr='.addr.')')
        [snip]
```

Lets run the emulator again and see if the log file contains any information.

```bash
# We add `-c q` to exit vim after the file and been read and the emulator has
# finished running. This isn't important but saves a couple of seconds of my
# life
$ vim -S sky.vim vuln.sky -c q
$ cat sky.log
Connect(length=14, path=127.0.0.1:8765)
```

#### 4. How Does The Emulator `Connect()`?

This connect function looks interesting. Why is the program trying to
`Connect()`? Is it expecting a certain input? Can we modify what the program is
trying to do by connecting to it from the outside?

Looking at the `EmuSyscallConnect()` function, there is a `ch_open()` function
and a `ch_status()` function:

```vim
function! EmuSyscallConnect(state)

        let length = EmuPop(a:state)
        let path = EmuPopStr(a:state, length)
        call LogLine('Connect(length='.length.', path='.path.')')

        let channel = ch_open(path)
        if ch_status(channel) != 'open'
                let a:state['finish'] = 1
                return
        endif

        call EmuPushItem(a:state, channel)
endfunction
```

To learn more about the `ch_open()` function you can do `:help ch_open()` in
vim:

```vim
ch_open({address} [, {options}])                                ch_open()
                Open a channel to {address}.  See channel.
                Returns a Channel.  Use ch_status() to check for failure.

                {address} has the form "hostname:port", e.g.,
                "localhost:8765".
```

The above shows that a _channel_ is being opened with `ch_open()`.
`ch_status()` is used to check if we failed. But what's a channel? Moving to
the top of the help page it says:

```vim
Vim uses channels to communicate with other processes.
A channel uses a socket or pipes.                       socket-interface
```

Since we know "127.0.0.1:8765" is being passed to `ch_open()` we can try to act
as the _other process_ trying to communicate with vim.

#### 5. Learning More About Vim Channels

After reading more of the `ch_open()` help page you might come across a section
called "Channel Demo" (or just type `:help channel-demo`). This section says
there is a file, "demoserver.py", located at `$VIMRUNTIME/tools/demoserver.py`.
For some reason this file is not on my file system (even though I have vim
installed). Some Google'ing around leads to a file with the same name in the
"vim" repository on GitHub, which can be found
[here](https://github.com/vim/vim/blob/master/runtime/tools/demoserver.py).

After looking at demoserver.py it seems it is listening on port 8765 which is
the same port the emulator is trying to connect to. Let's try to run the python
script and the emulator:

```bash
# In terminal 1
$ python3 demoserver.py
[snip]

# In terminal 2
$ vim -S sky.vim vuln.sky -c q
```

After that, let's check the log file to see if anything different happened:

```bash
$ cat sky.log
Connect(length=14, path=127.0.0.1:8765)
Read(length=26, addr=0, data=Enter key to decrypt flag)
Read(length=5, addr=0, buf=80)
Close(addr=0)
Log(addr=90, length=44)
Gzz
   Syw<`f|#}KHl2_0}nV~Kg.FRz%@:
Exit()
```

It seems the emulator is sending the message "Enter key to decrypt flag" and is
reading five bytes. It's highly likely these five bytes could lead us to the
flag 😉

#### 6. Tracing The Instructions

It would be great to know what the program is actually doing. Since we've
traced all of the system calls that the program executes it would also help to
know the instructions as well. We can log the instructions that are executed by
adding another call to `LogLine()` in each function. We can also add the
arguments for each instruction to get a better idea of what the program is
doing.

But how do we know which functions are dealing with instructions? Well in
`SkyEmulator()` (the entry point into the program) there is a chain of
if-statements. It's very common for emulators to have big _switch statement_
for each of the instructions the emulator can emulate. Unfortunately, Vim
Script does not support switch statement but this is the closest thing we have:

``` vim
function! SkyEmulator()

        [snip]

        while (state['finish'] == 0) && (state['pc'] < len(state['text']))

                [snip]

                if opcode == 0x92
                        call EmuPush(state)
                elseif opcode == 0x6b
                        call EmuPop(state)
                elseif opcode == 0x5f
                        call EmuSyscall(state)
                elseif opcode == 0x0f
                        call EmuDup(state)
                [snip]
```

Going into each of the functions we can add out call to `LogLine()`

```vim
" NOTE: Not all functions are shown here

function! EmuPush(state)
        let pc = a:state['pc']
        let byte = a:state['text'][pc + 1]
        call PCInc(a:state, 1)
        call LogLine('Push(byte='.byte.')')
        [snip]

function! EmuLessThan(state)
        let a = EmuPop(a:state)
        let b = EmuPop(a:state)
        call LogLine('LessThan(a='.a.', b='.b.')')
        [snip]

function! EmuMod(state)
        let a = EmuPop(a:state)
        let b = EmuPop(a:state)
        call LogLine('Mod(a='.a.', b='.b.')')
        [snip]

...
```

Let's run the emulator again:

```bash
# NOTE: The demoserver.py script should be still running in the background
$ vim -S sky.vim vuln.sky -c q
```

#### 7. Cleaning Up The Disassembly

Looking at the disassembly in `sky.log` there seems to be a tonne of output,
over 2200 lines! It's difficult to understand what is going on with so much
noise. Is there anything in `sky.log` that we can remove to make our life
easier? Well over half of the lines in the file are `Push()` and `Pop()`
instructions as we can see below:

```bash
$ grep -a '^Pop\|^Push' sky.log | wc -l
1451
```

These instructions are only used to pass arguments to other instructions. This
can be seen in the source code of the emulator. For example, take the simple
function `EmuAdd()` which is used to add two numbers. The two numbers that are
added together are popped from the stack and the result is pushed back into the
stack:

```vim
function! EmuAdd(state)
        let a = EmuPop(a:state)
        let b = EmuPop(a:state)
        call EmuPushItem(a:state, a + b)
endfunction
```

To view the disassembly without the `Push()` and `Pop()` instructions we can
use the following command:

```bash
# `nl` prints the line numbers, this makes reading the disassembly easier to
# read.
$ grep -va '^Pop\|^Push' sky.log | nl -s '. '
     1.  Syscall(sysnum=2)
     2.  Connect(length=14, path=127.0.0.1:8765)
     3.  Poke(addr=0, item=channel 0 open)
     4.  Syscall(sysnum=4)
     5.  Send(length=26, addr=0, data=Enter key to decrypt flag)
     6.  Syscall(sysnum=3)
     7.  Read(length=5, addr=0, buf=80)
     8.  Syscall(sysnum=5)
     9.  Close(addr=0)
    10.  MemCopy(addr=90, length=44)
    11.  Dup(offset=2)
    12.  Dup(offset=2)
    13.  LessThan(a=0, b=44)
    14.  IsZero(tmp=1)
    15.  JumpCond(offset=28, cond=0)
[snip]
```

#### 8. Patterns In The Disassembly

After looking at the disassembly for a while it looks like some of the
instructions are being repeated every few lines:

```txt
11. Dup(offset=2)                | 29. Dup(offset=2)               | 47. Dup(offset=2)
12. Dup(offset=2)                | 30. Dup(offset=2)               | 48. Dup(offset=2)
13. LessThan(a=0, b=44)          | 31. LessThan(a=1, b=44)         | 49. LessThan(a=2, b=44)
14. IsZero(tmp=1)                | 32. IsZero(tmp=1)               | 50. IsZero(tmp=1)
15. JumpCond(offset=28, cond=0)  | 33. JumpCond(offset=28, cond=0) | 51. JumpCond(offset=28, cond=0)
16. Dup(offset=1)                | 34. Dup(offset=1)               | 52. Dup(offset=1)
17. Add(a=90, b=0)               | 35. Add(a=90, b=1)              | 53. Add(a=90, b=2)
18. Peek(addr=90)                | 36. Peek(addr=91)               | 54. Peek(addr=92)
19. Dup(offset=3)                | 37. Dup(offset=3)               | 55. Dup(offset=3)
20. Mod(a=0, b=5)                | 38. Mod(a=1, b=5)               | 56. Mod(a=2, b=5)
21. Add(a=80, b=0)               | 39. Add(a=80, b=1)              | 57. Add(a=80, b=2)
22. Peek(addr=80)                | 40. Peek(addr=81)               | 58. Peek(addr=82)
23. Xor(a=119, b=48)             | 41. Xor(a=104, b=18)            | 59. Xor(a=97, b=27)
24. Dup(offset=2)                | 42. Dup(offset=2)               | 60. Dup(offset=2)
25. Add(a=90, b=0)               | 43. Add(a=90, b=1)              | 61. Add(a=90, b=2)
26. Poke(addr=90, item=71)       | 44. Poke(addr=91, item=122)     | 62. Poke(addr=92, item=122)
27. Add(a=1, b=0)                | 45. Add(a=1, b=1)               | 63. Add(a=1, b=2)
28. Jump(offset=219)             | 46. Jump(offset=219)            | 64. Jump(offset=219)
```

A sequence of repeating instructions that start with a comparison (lines 13,
31, and 49) and end in a jump (lines 28, 46, and 64)? That sounds like a loop
to me!

Right before the jump there's an add instruction which increments something by
1 (as seen in lines 27, 45, and 63). So it's not just any type of loop but a
for loop!

#### 9. Deconstructing The For-loop

With our knowledge that there is probably a for loop, we can reconstruct the
code into pseudo-C (using lines 11 to 28).


```C
for(i = 0; i < 44; i++) {

    Dup(offset=1)
    Add(a=90, b=0)
    Peek(addr=90)

    Dup(offset=3)
    Mod(a=0, b=5)
    Add(a=80, b=0)
    Peek(addr=80)

    Xor(a=119, b=48)
    Dup(offset=2)
    Add(a=90, b=0)
    Poke(addr=90, item=71)
}
```

The code can be split into three main chunks; two of the chunks call `Peek()`
and the other one calls `Poke()`. What are these strange functions? Looking
at the source code for both of these functions show:

```vim
function! EmuPeek(state)
        let addr = EmuPop(a:state)
        let item = a:state['as'][addr]
        call EmuPushItem(a:state, item)
endfunction

function! EmuPoke(state)
        let addr = EmuPop(a:state)
        let item = EmuPop(a:state)
        let a:state['as'][addr] = item
endfunction
```

It seems the `Peek()` instruction will read something from the address space
at the address `addr` and push the result onto the stack. The `Push()`
instruction will pop the `addr` and `item` off the stack and store the `item`
into the address space at `addr`.

Let's look at the execution of the first chunk during the program:

```txt
+---------------------+---------------------+----------------------+----------------------+
|  16. Dup(offset=1)  | 34. Dup(offset=1)   | 52. Dup(offset=1)    | 70. Dup(offset=1)    |
|  17. Add(a=90, b=0) | 35. Add(a=90, b=1)  | 53. Add(a=90, b=2)   | 71. Add(a=90, b=3)   |
|  18. Peek(addr=90)  | 36. Peek(addr=91)   | 54. Peek(addr=92)    | 72. Peek(addr=93)    |
+---------------------+---------------------+----------------------+----------------------+
|  88. Dup(offset=1)  | 106. Dup(offset=1)  | 124. Dup(offset=1)   | 142. Dup(offset=1)   |
|  89. Add(a=90, b=4) | 107. Add(a=90, b=5) | 125. Add(a=90, b=6)  | 143. Add(a=90, b=7)  |
|  90. Peek(addr=94)  | 108. Peek(addr=95)  | 126. Peek(addr=96)   | 144. Peek(addr=97)   |
+---------------------+---------------------+----------------------+----------------------+
| 160. Dup(offset=1)  | 178. Dup(offset=1)  | 196. Dup(offset=1)   | 214. Dup(offset=1)   |
| 161. Add(a=90, b=8) | 179. Add(a=90, b=9) | 197. Add(a=90, b=10) | 215. Add(a=90, b=11) |
| 162. Peek(addr=98)  | 180. Peek(addr=99)  | 198. Peek(addr=100)  | 216. Peek(addr=101)  |
+---------------------+---------------------+----------------------+----------------------+
```

Looking at the execution of the first chunk (above) it seems that the program
is peek'ing a byte on each iteration of the loop and the address is also being
incremented. It's possible the chunk evaluates to `tmp1 = array1[i]`.

Let's look at the execution of the second chunk:

```txt
+---------------------+---------------------+---------------------+---------------------+
|  19. Dup(offset=3)  | 37. Dup(offset=3)   | 55. Dup(offset=3)   | 73. Dup(offset=3)   |
|  20. Mod(a=0, b=5)  | 38. Mod(a=1, b=5)   | 56. Mod(a=2, b=5)   | 74. Mod(a=3, b=5)   |
|  21. Add(a=80, b=0) | 39. Add(a=80, b=1)  | 57. Add(a=80, b=2)  | 75. Add(a=80, b=3)  |
|  22. Peek(addr=80)  | 40. Peek(addr=81)   | 58. Peek(addr=82)   | 76. Peek(addr=83)   |
+---------------------+---------------------+---------------------+---------------------+
|  91. Dup(offset=3)  | 109. Dup(offset=3)  | 127. Dup(offset=3)  | 145. Dup(offset=3)  |
|  92. Mod(a=4, b=5)  | 110. Mod(a=5, b=5)  | 128. Mod(a=6, b=5)  | 146. Mod(a=7, b=5)  |
|  93. Add(a=80, b=4) | 111. Add(a=80, b=0) | 129. Add(a=80, b=1) | 147. Add(a=80, b=2) |
|  94. Peek(addr=84)  | 112. Peek(addr=80)  | 130. Peek(addr=81)  | 148. Peek(addr=82)  |
+---------------------+---------------------+---------------------+---------------------+
| 163. Dup(offset=3)  | 181. Dup(offset=3)  | 199. Dup(offset=3)  | 217. Dup(offset=3)  |
| 164. Mod(a=8, b=5)  | 182. Mod(a=9, b=5)  | 200. Mod(a=10, b=5) | 218. Mod(a=11, b=5) |
| 165. Add(a=80, b=3) | 183. Add(a=80, b=4) | 201. Add(a=80, b=0) | 219. Add(a=80, b=1) |
| 166. Peek(addr=83)  | 184. Peek(addr=84)  | 202. Peek(addr=80)  | 220. Peek(addr=81)  |
+---------------------+---------------------+---------------------+---------------------+
```

This chunk seems similar to the previous chunk however the index is `i % 5`.
It's possible this chunk evaluates to `tmp2 = array2[i % 5]`.

Let's look at the execution of the third chunk:

```txt
+------------------------------+------------------------------+-------------------------------+
|  23. Xor(a=119, b=48)        | 41. Xor(a=104, b=18)         | 59. Xor(a=97, b=27)           |
|  24. Dup(offset=2)           | 42. Dup(offset=2)            | 60. Dup(offset=2)             |
|  25. Add(a=90, b=0)          | 43. Add(a=90, b=1)           | 61. Add(a=90, b=2)            |
|  26. Poke(addr=90, item=71)  | 44. Poke(addr=91, item=122)  | 62. Poke(addr=92, item=122)   |
+------------------------------+------------------------------+-------------------------------+
|  77. Xor(a=116, b=127)       | 95. Xor(a=63, b=59)          | 113. Xor(a=119, b=36)         |
|  78. Dup(offset=2)           | 96. Dup(offset=2)            | 114. Dup(offset=2)            |
|  79. Add(a=90, b=3)          | 97. Add(a=90, b=4)           | 115. Add(a=90, b=5)           |
|  80. Poke(addr=93, item=11)  | 98. Poke(addr=94, item=4)    | 116. Poke(addr=95, item=83)   |
+------------------------------+------------------------------+-------------------------------+
| 131. Xor(a=104, b=17)        | 149. Xor(a=97, b=22)         | 167. Xor(a=116, b=72)         |
| 132. Dup(offset=2)           | 150. Dup(offset=2)           | 168. Dup(offset=2)            |
| 133. Add(a=90, b=6)          | 151. Add(a=90, b=7)          | 169. Add(a=90, b=8)           |
| 134. Poke(addr=96, item=121) | 152. Poke(addr=97, item=119) | 170. Poke(addr=98, item=60)   |
+------------------------------+------------------------------+-------------------------------+
| 185. Xor(a=63, b=48)         | 203. Xor(a=119, b=23)        | 221. Xor(a=104, b=14)         |
| 186. Dup(offset=2)           | 204. Dup(offset=2)           | 222. Dup(offset=2)            |
| 187. Add(a=90, b=9)          | 205. Add(a=90, b=10)         | 223. Add(a=90, b=11)          |
| 188. Poke(addr=99, item=15)  | 206. Poke(addr=100, item=96) | 224. Poke(addr=101, item=102) |
+------------------------------+------------------------------+-------------------------------+
```

Looking at the above chunk it seems the first argument for the `Xor()` function
repeats on each fifth iteration. The result of the xor operation is also
poke'ed back into memory. For example, line 23 will `Xor(119, 48) == 71` and
store the result on line 26. The code for the above chunk is probably
`array1[i] = tmp3 ^ tmp4`.

#### 10. Back to C

The pseudo-C code should now look something like the following:

```C
for(i = 0; i < 44; i++) {
    tmp1 = array1[i];
    tmp2 = array2[i % 5];
    array1[i] = tmp3 ^ tmp4;
}
```

But what are these `tmp*` values? Let's modify the logging function in
`EmuPeek()` to show the value it read:

```vim
function! EmuPeek(state)
        let addr = EmuPop(a:state)
        let item = a:state['as'][addr]
        call LogLine('Peek(addr='.addr.') -> ' . item)
        call EmuPushItem(a:state, item)
endfunction
```

After running the emulator again we get the following output:

```
[snip]
    16. Dup(offset=1)
    17. Add(a=90, b=0)
    18. Peek(addr=90) -> 48

    19. Dup(offset=3)
    20. Mod(a=0, b=5)
    21. Add(a=80, b=0)
    22. Peek(addr=80) -> 119

    23. Xor(a=119, b=48)
    24. Dup(offset=2)
    25. Add(a=90, b=0)
    26. Poke(addr=90, item=71)
[snip]
```

It seems the value stored on line 26 is the result of xor'ing of the two calls
to `Peek()`. The pseudo-C code should now look something like the following:

```C
for(i = 0; i < 44; i++) {
    array1[i] = array1[i] ^ array2[i % 5];
}
```

#### 11. Understanding The Encryption

If we recall the second chunk of the for loop (below) the call to `Peek()`
seems interesting.

```txt
    19. Dup(offset=3)
    20. Mod(a=0, b=5)
    21. Add(a=80, b=0)
    22. Peek(addr=80) -> 119
...
    40. Peek(addr=81) -> 104
...
    58. Peek(addr=82) -> 97
...
    76. Peek(addr=83) -> 116
...
    94. Peek(addr=84) -> 63
...
```

Each of these `Peek()` instructions seem to return ASCII values which can be
seen below:

| Line | Peek(80 + (i % 5)) | ASCII |
|------|--------------------|-------|
| 23.  | 119                | `w`   |
| 41.  | 104                | `h`   |
| 59.  | 97                 | `a`   |
| 77.  | 116                | `t`   |
| 95.  | 63                 | `?`   |

It seems this is the _key_ which was returned by the `demoserver.py` script!
This can be seen from the code extract below:

```python
[snip]
else:
    response = "what?"
encoded = json.dumps([decoded[0], response])
print("sending {0}".format(encoded))
self.request.sendall(encoded.encode('utf-8'))
[snip]
```

We can now update our pseudo-C code:

```C
for(i = 0; i < 44; i++) {
    array1[i] = array1[i] ^ key[i % 5];
}
```

This smells like an [xor cipher](https://en.wikipedia.org/wiki/XOR_cipher)!
Therefore, `array1` is probably the `flag` that we are looking for. Let's
update our pseudo-C code again:

```C
for(i = 0; i < 44; i++) {
    flag[i] = flag[i] ^ key[i % 5];
}
```

#### 12. Extracting The Encrypted Flag

Let's extract the encrypted flag and see if we can find the clear text. By
extracting all of the `Peek()` instructions in the for-loop for the flag will
give the following list

```python
encrypted_flag = [
    48, 18, 27, 127, 59, 36, 17, 22,
    72, 48, 23, 14, 29, 87, 66, 60,
    32, 13, 70, 45, 8, 55, 114, 68,
    45, 10, 6, 55, 96, 65, 60, 15,
    115, 126, 45, 89, 46, 51, 108, 69,
    82, 109, 33, 78,
]
```

#### 13. Decrypting The Flag

Since we know what the encrypted flag is all we have to do is decrypt it :D

We know the key is five characters since each index in the key array is indexed
modulo five. Since we know the flag starts with `SKYLI` we can try to decrypt
the first five characters.

| Index | Encrypted Byte | Real Key `ASCII`| Result `ASCII` |
|-------|----------------|-----------------|----------------|
| 0     | 48             | 99 `c`          | 83 `S`         |
| 1     | 18             | 89 `Y`          | 75 `K`         |
| 2     | 27             | 66 `B`          | 89 `Y`         |
| 3     | 127            | 51 `3`          | 76 `L`         |
| 4     | 59             | 114 `r`         | 73 `I`         |

So the real key is `[99, 89, 66, 51, 114]` or `cYB3r` in ASCII. Using the
python script below it's possible decrypt the flag:

```python
encrypted_flag = [
    48, 18, 27, 127, 59, 36, 17, 22,
    72, 48, 23, 14, 29, 87, 66, 60,
    32, 13, 70, 45, 8, 55, 114, 68,
    45, 10, 6, 55, 96, 65, 60, 15,
    115, 126, 45, 89, 46, 51, 108, 69,
    82, 109, 33, 78,
]

key = [99, 89, 66, 51, 114]

flag = ''
for i in range(len(encrypted_flag)):
    flag += chr(encrypted_flag[i] ^ key[i % 5])

print(flag)
```

If you're smart enough to get to here in the write up then you should be smart
enough to run a python script ... but just in case you don't know:

```
$ python3 hak.py
SKYLIGHT{BtW_d0_yOu_kn0w_i_uS3_V1M_:wq_714c}
```

### Flag

```
SKYLIGHT{BtW_d0_yOu_kn0w_i_uS3_V1M_:wq_714c}
```

</details>
