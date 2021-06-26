# re workshop

## Authors
- @abiramen

## Category
- Misc

## Description
I hear that Skylight Cyber is presenting a talk on reverse engineering with Ghidra for SecSoc soon! I wonder when that's occurring.

Find the Unix time that the talk is scheduled to start (in milliseconds), and wrap it with `SKYLIGHT{}`.

## Difficulty
- Easy

## Points
5

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- Find out about a cool event that Skylight and SecSoc are running.
- Learn about Unix time.

### Walkthrough
1. Find the date and time of the workshop on the SecSoc homepage to be Monday 19 July 2021 at 2pm.
2. Find an online Unix time converter and enter the above date and time in. Note that some websites give Unix times in seconds, so you may need to multiply your number by 1000.

### Flag
`SKYLIGHT{1626667200000}`
</details>
