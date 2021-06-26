# runaway diplomat

## Authors
- @abiramen

## Category
- Recon

## Description
We highly suspect that a diplomat who was at a foreign embassy was actually here for intelligence purposes.

However, they've suddenly fled the country. They accidentally left a USB behind though, and it seems that they've been spying on live satellite feeds of some of our airports.

We haven't been able to identify this airport yet though. Can you help us? **You can assume that magnetic north is directly up in the image.**

Your flag should be the ICAO code for the airport, wrapped with `SKYLIGHT{}`. For example, if this was Sydney Airport, your flag would be `SKYLIGHT{YSSY}.

**Do not attempt to brute force this challenge.** We will be monitoring submission logs.

**Note**: This airport may be anywhere in the world.

## Difficulty
- Medium

## Points
125

## Files
- sat_img_01.png: A satellite image of some airport.

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- Identifying runway markings, and how runway numbering works.

### Walkthrough
1. A good place to start is to look at a nearby airport, and identifying what distinguishing features it has. If we look at Sydney Airport, we see that it has 3 runways, with distinctive yellow chevron markings on each end. We can zoom in on each runway, and see that they have numbers on each end - the two perpendicular runways are 16L-34R and 16R-34L, and the other runway has number 7-24. Now's a good time to google how runway numbers work.
    - We can learn that runways at all ICAO airports are numbered between 1 and 36, depending on their compass heading - that is, their bearing from magnetic north. Runway number 18, for example, would be towards the south at a bearing of 175-185 degrees, and runway 36 would be the same runway, in the opposite direction.
    - Parallel runways have the extra letters 'L' or 'R' affixed to them, specifying whether runway is on the left or right. In the case of three runways, such as at Memphis International Airport (KMEM) for example, the middle runway is labelled 'C' for centre.
2. We've conveniently been told that the satellite image has been oriented with magnetic north being upwards. From this, we can roughly estimate the runway numbers of the three runways (identifiable by the yellow chevrons, with one runway being slightly cropped out but still identifiable) in the image. We can see that 2 of them seem to be parallel, and the third seems to be perpendicular. We can now use a protractor to estimate the headings of these runways. We can see that the parallel runways seem to be at about 6 degrees from north (or 186 degrees in the other direction). This means that we can assume that the two parallel runways are numbered 1L-19R and 1R-19L. As the other runway is roughly perpendicular to the other two, we know that it should be runway 10-28.
3. Since most airports in the world don't have the same combination of runways, we can google for "runway 1l-19r 1r-19l 10-28". The first four search results seem to be for Tampa International Airport (KTPA). If we look at satellite imagery for this airport, we can identify that we have a match!

### Flag
`SKYLIGHT{KTPA}`

### Notes
Image taken from Google Maps Satellite view and rotated to match magnetic north.
</details>
