#!/usr/bin/python3
"""
Encodes a zero-indexed book cipher, with tuples being (word number, letter number)
Hacked together by @abiramen for a CTF.
Reused and modified by @damo190 for another CTF (thanks abiram)
"""

from sys import exit
from random import choice

book_path = input("What is the path to your book? ")

letters = {}
word_count = 0
with open(book_path) as book:
    for line in book.readlines():
        for word in line.split():
            for index, letter in enumerate(word):
                if letter.lower() not in letters:
                    letters[letter.lower()] = []
                letters[letter.lower()].append((word_count, index))
            word_count += 1

to_encode = input("What string would you like to encode? ").lower()

for c in to_encode:
    if c not in letters:
        print("Whoops, the letter {c} doesn't occur in the book.")
        exit()
    print(str(choice(letters[c])[0]) + " " + str(choice(letters[c])[1]), end=" ")
