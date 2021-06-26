#!/usr/bin/python3
# SKYLIGHT{hop3_y0u_Lik3_m0duLus}
import pwn
start_string = "skylight_cyb3r"
p = pwn.process("vuln")
index = 0
new_str = ""
for i in range(0, 14):
    index += 5
    new_str += start_string[index % len(start_string)]

p.sendline(new_str)
pwn.log.info(p.readline())
