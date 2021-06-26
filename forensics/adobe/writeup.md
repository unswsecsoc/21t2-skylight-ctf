# Title

## Authors
- @joooooooooooooooooooooooooooooooooooosh

## Category
- Forensics

## Description
I've made my own document format, but it's not very readable...

## Difficulty
- Easy

## Points
50

## Files
- combined.pdf: PDF with a malformed JPEG appended to it

## Solution
<details>
<summary>Spoiler</summary>

### Idea
PDF readers ignore any data past the end of file signature in a PDF, so we can create an innocuous (but suspiciously blank) PDF file with some juicy secrets hidden at the end of it.

### Walkthrough
1. The standard way to mark the end of a PDF file is through the byte sequence %%EOF (or 0x2525454f46). However, the given PDF file is ~8x larger than a regular blank PDF, implying there's some extra information hidden.

2. If you look for the EOF marker in `combined.pdf`, you can see that there's plenty of extra data.

    - In particular, running `xxd combined.pdf | grep EOF` outputs `00000e10: 454f 460a 0a0a ffe0 0010 4a46 4946 0001  EOF.......JFIF..`
    - JFIF is part of the header of a JPEG file, but the first few bytes seem to have been replaced by 0x0a.

3. We can extract the data by removing the PDF part of the binary. There are several ways to do this, but I used `tail`. Thanks to the `xxd` output, we know that the last line of the PDF file started at 0xe10 and finished 4 bytes in, so the PDF file is 0xe14 (or 3604) bytes long. 
    - Running `tail -c +3605 combined.pdf > test.jpeg` will remove the PDF part of the file, leaving just the JPEG behind.
    - Now we need to put the magic bytes back. https://en.wikipedia.org/wiki/List_of_file_signatures tells us that the headers for JPEGs start with FF D8 FF E0, so we just need to patch the fist two bytes of our new file.
    - There are probably much neater ways to do this, but my first instinct was to reuse the `tail` idea by writing the first two bytes and then appending the rest of the `test.jpeg` file, skipping the first two bytes.
    - `echo -en "\xff\xd8" > final.jpeg; tail -c +3 test.jpeg >> final.jpeg` creates our perfectly formatted image. Open this in any image viewer and the text is easy to see.

### Flag
`SKYLIGHT{n3v3r_trUst_th3_h3ad3rs}`
</details>
