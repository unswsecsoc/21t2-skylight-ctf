# Title
Bubsy 3D was good.

## Authors
- @damo190

## Category
- Misc

## Description
I've been reading the 1996 Gamespot review of the legendary Bubsy 3D for the Playstation and they are saying some really strange things like it is supposedly a "terrible game", luckily my local hacker friend gave me a code that should prove the true quality of this masterpiece, I just can't quite figure out the code...

Wrap your found result in SKYLIGHT{}.

## Difficulty
- Medium

## Points
75

## Hints
1. ...
1. ...

## Files
- code.txt: Has the book cipher code


## Solution
<details>
<summary>Spoiler</summary>

### Idea
The general idea is to first scour the internet for an article before applying a book cipher to the found article.

### Walkthrough
1. The text file is simply a string of numbers, it doesn't seem like there is much use of them, so when the file makes little to no sense, it is important to look into what we can find from the description.
2. The description quite abruptly mentions a year, company, and name of a game, a quick Google search gets you onto a website with an archive of an old videogame review for the titular Bubsy 3D.
3. Okay now we have some text.... great, the next step is to revisit the code and the string of numbers we have there, you will notice, while random, the numbers actually come in pairs. There is large number which is followed by a smaller on and this is repeated. 
4. With this realisation in mind, the astute elite hax0r will know of this as a book cipher, or for those have not seen such before, here is a brief explanation of the code.

    - The larger numbers refer to the index of a word within the text, each word is given an index, with the first word having the index 0 and the second word having the index 1 and so on (this process is known as enumeration).
    - The smaller numbers refer to the index of the letter within the word index by the larger number, with the first letter having the index of 0 and the second letter having the index of 1 and so on (another enumeration).

5. With this, a script of some sort can be written in ones favourite language to find the cipher and crack it, below is a simple python script that (messily) does the job

```
text = """Bubsy the Bobcat is the most annoying kitty in all of gamedom - simply because Accolade's tried so hard to shove their would-be mascot down gamers' throats. The original Bubsy was a weak Super Mario/Sonic rip-off with one unbelievably major flaw: the player died after taking a SINGLE hit. Bubsy II was better, with tighter level design and weapon power-ups (although one of them was a Nerf Ballzooka, providing for a very ignoble product tie-in; try to imagine Mario wielding a Super Soaker 2000). Yet the sequel still suffered from the fundamental problem of a very irritating lead character. Does Bubsy 3D have graphics and gameplay good enough to overcome Bub and his endless barrage of cat puns? Not quite.

Bubsy 3D uses the third-person, behind-the-character view as seen in Mario 64 and Tomb Raider. Only here it's combined with mundane jumping/shooting/gliding action. (For reasons never explained in any of his game incarnations, Bubsy has the flying squirrel-esque ability to glide downward after jumping.) As players explore each level, they collect atoms (instead of coins/rings/wool), jump on or shoot the assortment of alien enemies, and search for rocket parts (the game's "cool secrets" component). But the controls don't feel right - Bubsy's inertia is off, which makes the jumps more frustrating than they should be (and jumping is activity No. 1 in an action/platform game). There's just not a gameplay hook here.

If the screen shots look particularly blah, it's because Bubsy 3D's designers decided to use the Playstation's high-res graphic mode (in the game's only hint of innovation), usually reserved for title screens. The resulting polygonal worlds are detailed and cartoony, but extremely sparse, and the ugly texture maps barely help. There's also a "fogging" effect which keeps Bubsy from seeing more than a few hundred feet in front of him - which is rather noticeable only when watching someone else play. The animation is slightly stiff (except for the excellent animated vignettes that play when the game is paused!). In short, Bubsy moves nowhere near as smoothly as Lara, the heroine in Tomb Raider, or Crash Bandicoot.

The music is extremely annoying - the composer succeeded all too well at capturing the sound of a Saturday morning theme song (and the sound effects are merely average). Thank god the programmers included an option to turn off the sound bites Bubsy spews during the game; after having to endure that lispy, grating voice two or three times, the player may be tempted to kill his or her television.

Of all the 3-D action/platform games out for the Playstation, Bubsy 3D is the least fun, and it is a title that's best rented not bought."""

#Change our string to a list without any new lines characters
formatted = text.strip().split()

code = "220 0 412 0 125 6 40 3 131 1 311 2 422 1 441 0 131 1 267 4 22 5 356 2 367 1 227 0 354 0 357 3 183 3 83 1 163 5"

#flip flop variable to go between getting the bigger and smaller number
big = True

#variables to store the large and small numbers
beeg_num = 0
smol_num = 0

#loop through the code
for num in code.split():
    if big:
        #if we are looking at the big number, we store it, flip our boolean and go to the next iteration of the loop
        big = False
        beeg_num = num
        continue
    else:
        #now we flip back to ensure we keep looping properly, before printing out the letter we have found in our text
        big = True
        smol_num = num

        print(formatted[int(beeg_num)][int(smol_num)], end = "")
        


```
6. This prints the flag :)

### Flag
`SKYLIGHT{1t-w4s-b4d-mAn-cm0n}`
</details>
