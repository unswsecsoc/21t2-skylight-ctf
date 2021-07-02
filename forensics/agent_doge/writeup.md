# Agent Doge

## Authors
- [@hexDoor](https://github.com/hexDoor)

## Category
- Forensics

## Description
At great personal risk, Agent Doge has managed to exfiltrate the download folder of a radical UNSW SecSoc executive.

What are they hiding from us?

## Difficulty
- Hard

## Points
225

## Hints
1. you won't ever find the password. try a different approach

## Files
- leaked_files: zip file containing challenge resources
- download.zip: encrypted zip file containing interesting info
- secret.md: plaintext that was not deleted (deliberately)

## Solution
<details>
<summary>Spoiler</summary>

### Idea
Encrypted ZIP KPA (bad thing with linux ZIP 3.0) - Known Plaintext Attack

### Walkthrough
1. `secret.md` hints that there's a secret within `download.zip`
2. `secret.md` also exists within the `download.zip` where the context in the text of `secret.md` most likely hints that it exists within the zip as well
3. zip files are able to be cracked via a KPA (known plaintext attack) which is heavily documented as a weakness for encrypted zip files
4. utilise a program called [`pkcrack`](https://github.com/keyunluo/pkcrack) which implements a published algorithm into cracking encrypted zip files
5. prepare a `plain.zip` by compressing `secret.md` again (Note: very important that Linux zip 3.0 is utilised as per `pkcrack` instructions)
6. run pkcrack `pkcrack -C download.zip -c secret.md -P plain.zip -p secret.md -d decrypt -a`
7. decrypted and unzipped `access_key` contains a base64 encoded string
8. flag GET

### Flag
`SKYLIGHT{hah4_secs0c_Sh0Rts_Dog3_c0iN}`
</details>
