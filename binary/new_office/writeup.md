# Title

New Office

## Authors

- @jame (Frank)
- @Sequeli (Atharv)

## Category

- Binary Exploit

## Description

We aren't using gets this time so good luck trying to execute a buffer overflow

`nc pwn.ctf.unswsecurity.com 5001`

## Difficulty

- Easy

## Points

50

## Files

- [new_office](_ctfd/files/new_office): binary to exploit

Try include a link to the file where possible (such as within a repo).

## Solution

<details>
<summary>Spoiler</summary>

### Idea

Use buffer overflow to redirect code execution!

### Walkthrough

1. As usual, a plug for LiveOverflow is due:

- [LiveOverflow's binary exploitation playlist](https://www.youtube.com/watch?v=iyAyN3GFM7A&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN)
  (Shall go into the exploits in MUCH more detail, is how @Sequeli learnt buffer overflows)

2. 

### Flag

`SKYLIGHT{3x3CuTe_0ff1cE_5TACK}`

</details>
