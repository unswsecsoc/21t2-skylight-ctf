# misrocoft orifice
This writeup will be updated soon with snippets of decompiled output.

## Authors
- @abiramen

## Category
- Reversing

## Description
i was recently out for a walk when i saw a small floppy disc for 'misrocoft orifice' fall off a truck ahead of me. it had this program on it, as well as some IP address?

`nc address port`

## Difficulty
- Medium

## Points
125

## Files
- misrocoft-orifice

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- Exploring different methods of string obfuscation
- Demonstrating why local license key verification is very hard to get right.

### Walkthrough
1. As always, when provided with a random file, there's a general series of steps you want to perform:
    - Run `file misrocoft-orifice` in order to determine its type - in this case, we're told that it's a 32-bit Linux ELF.
    - Use `strings filename` to see if we can determine anything about its behaviour this way.
    - Reverse-engineer it using the disassembler/decompiler/re suite of our choice, such as Ghidra, Radare2/Cutter or Binary Ninja.
    - Run it, preferably in a sandboxed environment if our re analysis was unable to determine if the binary was safe.
2. We can determine from our reversing that:
    - The program seems to read in our string, the license key, and pass pointers to different parts of the string to different functions, namely `cseg0`, `cseg2`, and `cseg3_4`. 
    - The program seems to explicitly check if characters 6-11 in the string match `LE4K5`, a string that is leaked from the binary.
    - If the return values of all of these checks are true, then the program calls an `open_document` function which seems to read from a file, presumably to print the flag when run on the remote server.
    - Looking at the cseg0 function, we can see the string 'BDQC3'. It's easy to assume that this is what's expected for the first 5 characters of the key, but closer inspection of the function reveals a loop which seems to iterate through each character of the string in reverse.
        - Your decompiled output might have some interesting pointer arithmetic like `*(array + 4 - i)`. It's worth noting that this is the same as `array[4-i]`.
        - We can now determine that this segment of the key is '3CQDB'.
    - Looking at the cseg2 function, we can see the usage of the XOR bitwise operator. More specifically, we can see that the next 5 characters of the string are iterated through, and compared with the bitwise XOR of individual bytes, using data found in readonly data in the binary.
        - We can take these bytes and XOR the first five from both to get `3CR0T`.
3. So far, our key is `3CQDB-LE4K5-3CR0T-?????-?????`. It seems that the last two segments are determined from the `cseg3_4` function, which takes two extra numbers as arguments.
    - The `cseg3_4` seems to pass the given segment of a string into a function called `val1`, and compares the first number with this argument. Taking a look at the decompiled output for the `val1` function, it seems to just be summing the (ASCII) value of each character in the segment.
    - The second `val2` function is harder to understand, even with its decompiled output. However, with some analysis, and maybe supplying some dummy values, we can deduce that it iterates through each character of the string, and computes the value of `(4 - i) * array[i]` and sums this value for each character together. That is, in the string ABCDE, the result of `val2` is determined to be `0 * 69 ('E') + 1 * 68 ('D') + 2 * 67 ('C') + 3 * 66 ('B') + 4 * 65 ('A')`. We thus need to find a string which matches the correct `val1` and `val2` for each segment. Particularly, we want `cseg3_4(&license_key[18], 308, 724) && cseg3_4(&license_key[24], 315, 690)` to be true.
    - We can write a Python script to efficiently bruteforce these.
    ```python
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
    ```
    - From this, we can determine solutions for the last two segments, of which there are several. A valid key would be `3CQDB-LE4K5-3CR0T-ZH200-MAA93`.
    - We can now connect to the remote and use this key to obtain the flag.
### Flag
`SKYLIGHT{cR4cK3d_My_0bfu$c4TeD_5tr!nGs}`
</details>
