# meowdy!

## Authors
- @abiramen

## Category
- Recon

## Description
so, i've just adopted a rescue cat and she's gorgeous. she's even got her own instagram page, and she made her first post over the past few days!

ooh, and the first few people to find her IG win a special treat! you can find all the deets you need [at this webpage](https://hi-howdy-meowdy.web.app/)! good luck 😻 

## Difficulty
- Medium

## Points
200

## Hints
1. and i need to stress, what three words will help you find me. [35 points]

## Solution
<details>
<summary>Spoiler</summary>

### Idea
- A few basic crypto/forensics techniques to find three words
- Linking clues to find a service to link these words to a location
- Looking at this location on social media

### Walkthrough
1. We can find the three words looking closely at the website:
    - `encrypted-1="yscnht" integrity="crwthvoxzapsqigymfjeldbunk"` in the HTML source for the page. We can identify that the integrity section is suspicious, as this doesnt look like a regular checksum, unlike those on the other lines. Googling this string, or looking closely at it, shows that it's a perfect pangram, containing all 26 characters of the alphabet, making it the perfect key for a substitution cipher. Applying it to 'yscnht' gives us our first word, nature.
    - The second word, `doll`, can be found by inspecting the comment in the EXIF data of the background image on the page.
    - The third word, `nature`, can be found in the following CSS snippet:
    ```css
    #word-three {
        background: #6E6174;
        color: #757265;
        display: none;
    }
    ```
    Each byte in the hex code for the colours is under 7F, meaning they could very easily be ASCII characters. Converting them, we get 'nat' and 'ure'.
2. Now that we've got three words, we can use the service what3words, which maps three words to unique locations around the world. Entering `played.doll.nature` gives us a location near Darlinghurst. Particularly, this location seems to be in 66 Foveaux Street, Surry Hills NSW. Googling this address gives us a cat address called Catmosphere.
3. We can now look for Catmosphere on Instagram. Visiting their instagram page or tagged photos doesn't reveal anything, but searching for recent images posted at the location gives us a recent post from an account called `@me0wfromskye`. Visiting this profile yields the string `}819d2f_eeeem_dNu0f_Evu_!YdwO3m{THGILYKS`, which is our flag in reverse.

### Flag
`SKYLIGHT{m3OwdY!_uvE_f0uNd_meeee_f2d918}`

### Notes
Unfortunately, the cat isn't real and was AI generated and taken from [https://thiscatdoesnotexist.com/].
</details>
