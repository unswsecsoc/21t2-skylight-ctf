# Title

## Authors
- @Charrd (Trin)

## Category
- Forensics

## Description
I went to a fortune teller but when they saw the message they refused to tell me! Im sure that they were a scam but I took a photo of the tea leaves anyway.

## Difficulty
- Easy

## Points
80

## Files
- tea_leaves: Image of a teacup with a hidden message.

## Solution
<details>
<summary>Spoiler</summary>

### Idea
Hiding image within another image

### Walkthrough
This walkthrough uses stegsolve but you just need a way to look at the LSB of each pixel in the image.
1. Open the image in stegsolve
2. Flick through the filters to either Green plane 0, Red plane 0 or Blue plane 0 to reveal the flag

### Flag
`SKYLIGHT{te4_Leav3s_@re_a_scAm}`
</details>
