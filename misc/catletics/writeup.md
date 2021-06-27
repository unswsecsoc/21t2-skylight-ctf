# catletics

Writeup coming soon!

## Authors
- @abiramen, heavily inspired by a CTF challenge from @lecafard in 2020.

## Category
- Misc

## Description
Due to budget cuts, Mathletics has become too expensive for my school to afford. I've decided to subscribe my students to Catletics instead. It's 95% cheaper, but requires students to connect using `nc pwn.ctf.unswsecurity.com 5008`, and has a 10 second time limit to save bandwidth.

I think it's an effective learning tool! I really hope none of my students know how to use pwntools...

## Difficulty
- Easy

## Points
50

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- Classic intro to pwntools maths challenge.

### Walkthrough
Solving random maths challenge within 10 seconds, you have to be either a
genius, or an entity that is capable of writing a script. Continue reading if
you identify with the latter.
1. Install `pwtools` with `python3 -m pip install pwntools`
2. We need to investigate what kind of maths we need to solve, to do this:
    * Use regex to find the expression, the pattern I used was: `What is (.*)\?`
    * Use python's `eval` function to evaluate the expression.
    * If it fails, make your script print out the most recent response.
    * From there, just add more regex to properly capture the expression and
      use appropriate methods to solve it.
3. The kinds of questions we need to solve:
    * Arithmetic operation of 2 numbers, can be solved with `eval`
    * Base convertion of numbers, can be solved with `eval` and any base
      convertion functions in python such as `int`, `oct`, `hex`, `bin`
    * Converting numbers to ASCII, can be solved with `eval` and `chr`
4. Complete your script by searching for the flags in each response before
   trying to solve the question, I used this regex pattern: `SKYLIGHT\{.*\}`
5. `./soln.py` -> ??? -> PROFIT

Also, `pwntools`
[documentation](https://docs.pwntools.com/en/stable/tubes.html) is helpful!


### Flag
`SKYLIGHT{pWnT00L5_m4St3R_0r%sC0Tt_fL4nsburG}`
</details>
