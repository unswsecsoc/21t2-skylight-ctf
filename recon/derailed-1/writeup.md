# derailed-1

## Authors
- @abiramen

## Category
- Recon

## Description
Find the following details about the pictured train accident and submit them as the flag.

`SKYLIGHT{nearesttown/suburb_date_approxtime_locomotivenumber_leftmosttrainregistration}`

For example:
- if the **nearest town/suburb** was Exampletown,
- the date of the pictured accident was 6 September 2020,
- the approximate time of the crash was 3:15pm local time,
- the number of the locomotive hauling the passenger train is A1234,
- the registration of the train in the left of the image is 5AB6,

the flag would then be `SKYLIGHT{exampletown_060920_1515_A1234_5AB6}`.

## Difficulty
- Easy

## Points
105

## Files
- derailed.png: A strangely distorted image, identical to that of derailed-0.

## Solution
<details>
<summary>Spoiler</summary>

### Walkthrough
1. We should now have the type of carriage and a bit more idea of what the train is from `derailed-0`. The other train pictured in the image appears to be a freight train, so we can Google "vline freight train accident", which yields [this ABC article](https://www.abc.net.au/news/2020-01-29/v/11911420) as a result. The imagery in this article seems to match the image we have! From this article, we have:
- the town (Barnawartha)
- the date (290120)
- a rough time (1740)
2. There is also a tweet embedded in the article, which has some more images of the accident. We can see an image of a locomotive, which appears to have the number `N474` on it. In case this wasn't clear, searching Twitter for 'barnawartha train' would've given more images from other journalists depicting the locomotive. We now have
- locomotive number (N474)
3. We just need the registration of the leftmost (freight) train. Googling for 'barnawartha train accident' gives us this report from the Australian Transport Safety Bureau, with the registration `4MC2`. We also get a better approximation of the time to be 1742. We now have all the details we need for the flag!

### Flag
`SKYLIGHT{barnawartha_290120_1742_N474_4MC2}`
</details>
