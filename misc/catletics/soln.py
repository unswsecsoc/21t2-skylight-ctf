#!/usr/bin/env python3

from pwn import remote
import re

URL = "<challenge URL>"
PORT = 420 # <challenge PORT>

FLAG_PATTERN = r"SKYLIGHT\{.*\}"

conn = remote(URL, PORT)

while True:
    try:
        # Get response from the remote URL,
        # either till EOF or 0.5 seconds has
        # elapsed
        raw_received = conn.recvrepeat(timeout=0.5)
    except Exception as e:
        # This means that we screwed up somewhere
        print(raw_received.decode("utf-8"))
        print(f"??? {e} ???")
        break

    received = raw_received.decode("utf-8")

    if re.search(FLAG_PATTERN, received):
        # When flag is found, print and break from loop
        conn.close()
        print(received)
        break

    if re.search(r"is (.*) in (.*)\?", received):
        # What is <number> in <base>?
        print("BASE CONVERT")
        line = re.search(r"is (.*) in (.*)\?", received)
        num = eval(line.group(1))
        base = line.group(2)
        if base == "hexadecimal":
            ans = hex(num)
        elif base == "decimal":
            ans = int(num)
        elif base == "octal":
            ans = oct(num)
        elif base == "binary":
            ans = bin(num)
        else:
            # unknown base, this lets us see what that is and allow us to
            # support more base in our script
            print(num, base)
            print(received)
            break
    elif re.search(r"What's (.*) as.* ([A-Z]+) .*\?", received):
        # What's <number> as an ASCII character?
        print("TO CHAR")
        line = re.search(r"What's (.*) as.* ([A-Z]+) .*\?", received)
        init = eval(line.group(1))
        ans = chr(init)
    elif re.search(r"What is (.*)\?", received):
        print("EVALUATE EXPR")
        # What is <number> + <number>
        line = re.search(r"What is (.*)\?", received)
        ans = eval(line.group(1))
    else:
        # New case that we have not handled, this shows us what the new case is
        print("WTF")
        print(received)
        break

    # send the answer
    conn.sendline(str(ans).encode("utf-8"))








