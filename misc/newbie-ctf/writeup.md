# newbie-ctf

## Authors
- @abiramen

## Category
- Misc

## Description
While this CTF has a wide variety of challenges with different difficulties, there's a SecSoc CTF just for beginners in collaboration with CSESoc soon!

Find the time that the CTF is scheduled to start in ISO8601 format (without separators, and using the same timezone as the event) and wrap it with `SKYLIGHT{}`.

Note: The contents of the flag should match the pattern `\d{8}\w\d{6}\+\d{4}`.
## Difficulty
- Easy

## Points
5

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- Find out about a cool event that SecSoc is running with the support of CSESoc.
- Learn about ISO8601 time formatting, which oddly has its own subreddit dedicated to it.

### Walkthrough
1. Find the date and time of the workshop on the SecSoc homepage to be Monday 19 July 2021 at 2pm.
2. Find an online ISO8601 time formatter and enter the above date and time in. Make sure to specify the timezone as UTC+10. You may need to make some modifications so that the time matches the given regular expression, and remove any hyphens or colons.

### Flag
`SKYLIGHT{20210716T100000+1000}`

### Other notes

I really, really intended for this challenge to be as simple as possible. I didn't anticipate how many variations of ISO8601 time people would come across (gotta love standards), and had to throw in a regular expression to help out a bit later, which still isn't extremely newbie friendly.
</details>
