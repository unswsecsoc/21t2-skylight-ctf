# Title

## Authors
- @damo190

## Category
- Crypto

## Description
Haha I just learnt about this RSA stuff and people are talking about it taking more than the heat death of the universe to crack! My data is secure you will never find out what my favourite number is. Note: When decrypted you will get a number, there is no need to wrap the number with SKYLIGHT{}.

## Difficulty
- Easy


## Points
000

## Hints
1. ...
1. ...

## Files
- highly_secretive_rsa.txt: Text file with secret code inside

Try include a link to the file where possible (such as within a repo).

## Solution
<details>
<summary></summary>

### Idea
An RSA encryption that has pathetically small prime numbers chosen that are easy to brute force calculate, encrypted is a fairly small number

### Walkthrough
1. A guide to encoding and decoding RSA encryption can be found on Wikipedia and other sources, the crux of the encryption is finding the prime factorisation of the public key. 
2. It is to be noted that we have 2 parts to the key, this is because RSA decryption involves using the key (the first number in the brackets) and the public exponent (the second number in the brackets) (Note: whilst it is not clear immediately which number is the key and the exponent, 37 is a prime number and so does not have an effective prime factorisation compared to 221). 
3. Factorising 221 gives you 13 x 17, we set these to be p and q respectively. (note: Normally with real RSA keys, this step would be practically impossible)
4. The totient (p-1) * (q-1) is calculated and found to be 12 * 16 = 192 and set to be phi
5. Using the public key, we need to solve the equation d*e = 1 (mod phi), a congruency equation which is akin to finding the value of x such that d = (1 + x * 192)/37 is an integer (x is also an integer). This step can be brute forced quite easily or even solved using online congruency calculators and d is found to be 109.
6. Now the encryption can be cracked as is infact the private exponent and the message can be decrypted by using the formula m = c^d (mod n) where c is the encrypted message sent (59), d was found in the prior step and n is the public key (221). Putting this together 59^109 (mod 221) is found to be 111, which is the flag.

### Flag
`111`
</details>
