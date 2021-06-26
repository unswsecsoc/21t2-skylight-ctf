# derailed-0

## Authors
- @abiramen

## Category
- Recon

## Description
Here's a weirdly distorted image of a train accident which I'm trying to research for a project...

Find the Wikipedia page for the type of passenger carriage featured in the image, and wrap the last section of the URL with Skylight. For example, if the answer was [https://en.wikipedia.org/wiki/New_Zealand_AK_class_carriage](https://en.wikipedia.org/wiki/New_Zealand_AK_class_carriage), the flag would be `SKYLIGHT{New_Zealand_AK_class_carriage}`.


## Difficulty
- Easy

## Points
50

## Files
- derailed.png: A strangely distorted image.

## Solution
<details>
<summary>Spoiler</summary>

### Walkthrough
1. Most Australian competitors will immediately identify that this image was taken in Australia, but the end of `000` on the side of the fire truck had reduced distortion to allow for a fairer playing field for any international competitors.
2. There's quite clearly a purple passenger train which we're looking for. Using Google Images for 'purple passenger train australia' gives us quite a few results for trains with what is clearly the same pattern on them, although not quite the same train. These trains all seem to be associated with the VLine in the state of Victoria.
3. We can now look at the Wikipedia page for the V/Line and find its operational fleet [here](https://en.wikipedia.org/wiki/V/Line#Rolling_stock).
4. There are two types of carriages which look remarkably similar to the one in the image -> the Z type carriage is very close to the N type, which was the correct answer here.

### Flag
`SKYLIGHT{VicRail_N_type_carriage}`

### Notes
- I had to work backwards to figure out what the carriage type was when writing this challenge, and I had also thought it was the Z type, until I used closer inspection of other imagery of the train crash (which you may find in the process of doing `derailed-1`). The main distinguishing external feature seems to be the size of the glass window on the rear door of each carriage.
    - It doesn't help that Wikipedia's imagery of the N type has it with older livery, rather than the newer geometric purple livery.
</details>
