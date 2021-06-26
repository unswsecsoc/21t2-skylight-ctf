# talking_cats

## Authors
- @damo190

## Category
- Crypto

## Description
My cats don't stop talking oh my, I swear the are out to get me or something. Every second of every day of every hour, the meowing continues, maybe they are trying to tell me something? I don't know how to make it stop, maybe if I figure out what they are trying to say...

## Difficulty
- Easy

## Points
50

## Hints
1. ...
1. ...

## Files
- please_make_it_stop.txt: Text file with secret code inside


## Solution
<details>
<summary></summary>

### Idea
Binary in text, 0s are meow, 1s are meowmeow. When transformed to binary and decoded to ASCII returns a Base64 string that when converted returns the flag

### Walkthrough
1. The given text file has a large string with one of two words repeated over and over, meow and meowmeow. There are a few forms of communication in which 2 distinct symbols are used to convey a message, morse code and binary should come to mind.

 - Morse Code however requires that we specify where the end of a letter and word is.
 - So binary seems like the obvious choice

2. This challenge requires you to figure out that the meowmeows are 1s and the meows are 0s, assuming the opposite would cause you to run into a wall. Once converted to binary and the binary converted to ASCII, the following string is returned:
>U0tZTElHSFR7dGgzX2NhdDVfYXIzX3Ixc2luZ191UH0=

Not obviously flaggy, but there is one striking clue about this string

3. The equals sign! If you haven't seen base64 encoded strings before, this will seem quite pointless but for those who have, the equals sign is a dead giveaway. Base64 is a number system with symbols to cover all numbers ranging from 0-63, most importantly, Base64 encoded strings must by size in bytes be divisble by 3.

>This is because Base64 encoding works by looking at the ASCII bits in groups of 6 instead of the usual group of 8, if the amount of bits is a multiple of 24 (a multiple of 3 bytes or 3 ASCII characters) then the encoding will occur seamlessly, otherwise padding must be added to the end of the string and this in Base64 is represented as '='.

Googling a Base64 Decoder and pasting the string above into it will output the flag :)

### Flag
`SKYLIGHT{th3_cat5_ar3_r1sing_uP}`
</details>
