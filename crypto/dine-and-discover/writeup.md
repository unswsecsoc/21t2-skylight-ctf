# Dine and Discover

## Authors
- @abiramen

## Category
- Crypto

## Description
My ramen restaurant is currently experiencing a power outage, and my front-of-house employee doesn't have a mobile data plan, and can't scan our customer's NSW Dine and Discover voucher.

They just called me to explain the situation, and asked me to scan the voucher on my end. They've sent the voucher over the phone as... a repeating series of beeps??? I can't figure out how to decode it.

Please help me out... they're really expecting a quick response.

You can listen in on the telephone line by connecting to it at `nc address port`.

Note: The 'telephone line' doesn't respond to any input.


## Difficulty
- Medium

## Points
125

## Solution
<details>
<summary></summary>

### Idea
- Receiving a stream of bytes from a remote
- Spotting patterns
- Operating on a stream of bytes

### Walkthrough
1. We notice that we get the same output whenever we connect to the remote address. This means that we should be able to save the output to a file, using `nc address port > output.txt`.
2. Looking at the output, your terminal may print out random strange characters and question marks. This suggests that the bytes we've received from the remote server (or 'telephone line') are likely not printable ASCII characters. It might be useful to view the bytes of this file with a hex editor, and we can do this with `hexdump output.txt` or preferably `xxd output.txt` if `xxd` is installed.
3. Looking closely, we can notice that the byte `0a` seems to occur every six bytes. Checking what `0a` represents, we see that it's a newline character in the ASCII table. It seems that it's being used to delimit output, or represent rows in our output.
4. Looking closely at the description, we can identify that this challenge may relate to QR codes, particularly since NSW Dine and Discover vouchers were in the form of QR codes, and this is further reinforced by 'expecting a quick response', which happens to be what QR stands for. This also links nicely with our theory about rows having a fixed width.
5. It might be useful to start using a language such as Python to process the bytes in our output.txt file. QR codes consist of a grid of squares, each being either black or white.
    - It might be plausible that each bit which forms the 5 bytes in each row represent a single black or white square.
    - We somehow need to take these bytes, convert them into bitstrings and then visualise those bits as black or white squares.
6. My method recommended method here is to export these bitstrings as comma-separated values, or CSVs -> for example, the first row of bytes becomes `1,1,1,1,1,1,1,0,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,0,0,0`. Since the file is now a CSV, we can open it with Google Sheets or Excel, and apply conditional formatting on our grid of cells, so that cells containing a 1 turn black, and cells containing a 0 remain white. We can then adjust the width of each column so that cells are squares. By the end of this process, we should have something that looks like a QR code.
7. We can now screenshot the result and use an online QR code scanner, or a tool like Google Lens to scan the QR code. We get the result `DINE AND DISCOVER U0tZTElHSFR7cHIwYjRCTHlfU2gwdUxkIV9qVXNUX3A0WV9mMFJfMW5UM3JOZVRfMWEzY2JlfQ==`.
8. We can take this base64 string (characterised by the equals signs on the end, which have a 2/3 chance of occuring with base64) and use a base64 decoder to get our flag.

### Flag
`SKYLIGHT{pr0b4BLy_Sh0uLd!_jUsT_p4Y_f0R_1nT3rNeT_1a3cbe}`

### Notes
- The process of me generating this challenge involved using Google Sheets to individually determine the colors of all 1369 squares in the QR code and set a cell to black and white, exporting it to CSV and then using a Python script.

    > converting a qr code to bits because i cant be bothered writing a script to extract it from the image

    > this will be the point we will later refer to as "where it all went wrong"

    > actually, conditional formatting makes this quite satisfying to do
- Row 20 of the original QR code for this challenge had bytes `bc 0a 93 2c e8`, which was a problem since `0a` was also the newline delimiter. I ended up having to flip a bit (since QR codes have amazing error correction and are pretty redundant to a few squares being incorrect) to remove the `0a` byte.
</details>
