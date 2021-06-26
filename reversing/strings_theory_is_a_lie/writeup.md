# Title

## Authors
- @joooooooooooooooooooooooooooooooooooosh

## Category
- Reversing

## Description
I didn't like using strcmp() so I implemented my own. Might be a bit more secure now that you can't get the answer straight from `strings`...

## Difficulty
- Easy

## Points
75

## Files
- vuln: redacted version of the binary

Try include a link to the file where possible (such as within a repo).

## Solution
<details>
<summary>Spoiler</summary>

### Idea
By torturing yourself with the raw assembly or using a decompiler, figure out how to get past the string check.

### Walkthrough
1. Open the binary in a tool with a decompiler such as Ghidra or Binary Ninja (Ghidra is free, Binary Ninja is free to demo and is generally more user friendly).
2. The decompiler will spit out some C code that reflects the underlying assembly. It's a bit hard to read, but if you look at the spicy_strcmp algorithm you can see the essentials:
    - There's a loop with a break condition
    - There are two counters, one which increments in steps of 1 and one which increments in steps of 5
    - Each loop, the first argument (your input) at the index of the 1-counter is compared to the second argument ("skylight_cyb3r") at the index of the 5-counter mod `strlen(second argument)`
    - If the comparison ever fails it returns 1, which we don't want
3. Make an input string that will pass the check.
    - Since we know the second string, we can emulate spicy_strcmp ourselves to create a string that will pass this check
    - This can be done manually, but I made a python script for it because I'm lazy

### Script
```python
#!/usr/bin/python3
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
```

### Flag
`SKYLIGHT{hop3_y0u_Lik3_m0duLus}`
</details>
