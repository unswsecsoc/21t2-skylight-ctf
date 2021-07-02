# Wall Street Bets ETF

## Authors
- [@hexDoor](https://github.com/hexDoor)

## Category
- Misc

## Description
It's a r/wallstreetbets ETF whitepaper.

What could possibly be bad about this new product?

## Difficulty
- Medium

## Points
150

## Hints
1. the pdf is not just a pdf

## Files
- whitepaper.pdf: file containing a hidden `secret.wav`

## Solution
<details>
<summary>Spoiler</summary>

### Idea
2 Stage Challenge - Essentially a binwalk + Slow Scan TV Robot36 audio file (in a zip) embedded

### Walkthrough
1. `whitepaper.pdf` has a filesize that's a little big for the content it contains
2. run a `binwalk` to see that there's a hidden `secret.wav`
3. playing the `secret.wav` seems to be outputting gibberish
4. the sounds are actually an image transmission method called [SSTV (Slow-scan television)](https://en.wikipedia.org/wiki/Slow-scan_television) (this one is in Robot36)
5. use an [SSTV decoder app available on android phones](https://play.google.com/store/apps/details?id=xdsopl.robot36&hl=en_AU&gl=US) (or others) to decode the transmission into an image
6. flag GET

### Flag
`SKYLIGHT{hah4_secs0c_Sh0Rts_Dog3_c0iN}`
</details>
