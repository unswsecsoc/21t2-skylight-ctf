#!/usr/bin/env python3

from Crypto.Cipher import AES
import sys

IV = b'\x19\xe7\x77\x79\x1f\xc2\xb9\x86\x42\x4e\x1b\x30\xbf\x0f\x72\xa5'
SECRET = b'U\xce\x91i\x16\xb1;e\x168\x93\xf7\x16~\x83R(\x8cq\x16\x0e3L\xb3`\xb0\xbd\xaa\x99]\xcc\x8f\xdd_o\xc7\x00\x14\x19\xee\xdbQ\xb2\xdd\xa9\xc6\x88\x11'

if len(sys.argv) != 2:
    print('+-----------------------------------------------------------+')
    print('| Usage: python3 printFlag.py <key>                         |')
    print('|                                                           |')
    print('| There are no bugs in this script... I hope.               |')
    print('|                                                           |')
    print('| By default, the `getFlag()` function will return 0. The   |')
    print('| goal of this challenge is to make `getFlag()` return 1.   |')
    print('| This can only be done by calling `setArrayValue()` with   |')
    print('| the correct key! Once you figure out this key give it to  |')
    print('| this script to decrypt and print the flag.                |')
    print('|                                                           |')
    print('| Good luck :D                                              |')
    print('+-----------------------------------------------------------+')
    sys.exit(1)

key = int(sys.argv[1]).to_bytes(32, byteorder='big')

flag = AES.new(key, AES.MODE_CBC, IV).decrypt(SECRET)
print(flag)
