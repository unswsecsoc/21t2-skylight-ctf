#!/usr/bin/python3
"""
Solves for the third and fourth segment of the license key for misrocoft orifice.
"""
from sys import argv, exit
import itertools, string

if len(argv) < 3:
    print('Usage: ./seg3_4.py val1 val2')    
    exit(1)

matches = []
for i in list(itertools.combinations_with_replacement(string.ascii_uppercase + string.digits, 5)):
    if sum([ord(j) for j in i]) == int(argv[1], 0):
        matches.append(i)

solve = ''

for match in matches:
    ordered = list(itertools.permutations(match, 5))
    for order in ordered:
        if sum([(4-i) * ord(x) for i, x in enumerate(order)]) == int(argv[2], 0):
            solve = ''.join(order)
            break
    if solve != '':
        break

print(solve)
