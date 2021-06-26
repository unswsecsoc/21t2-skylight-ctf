# HaCkInG ThE BlOcKcHaIn

This challenge was inspired by the talk "Outsmarting Smart Contracts" by
`Adi Ashkenazy` and `Shahar Zini`.

Source: https://www.youtube.com/watch?v=oO6XG3wm9QI

## Authors

- Jarrod Cameron

## Category

- Miscellaneous

## Description

I enjoy gambling which means I also enjoy investing in Ethereum.

I'm also a Computer Science student which means I only write bug free code.

Surely you can't exploit my code! It's bug free!

## Difficulty

- Child's Play

## Points

420

## Files

- printFlag.py: Script to decrypt the flag (this script doesn't contain any
  bugs and you can't brute force the key but you're welcome to try)
- vuln.sol: The vulnerable contract.

## Solution

<details>
<summary>Spoiler</summary>

### Idea

It's important to know the layout of objects in memory. Once you know how
Solidity stores objects this challenges becomes trivial. `&arr.length` is
located at `address 0`, `&flag` is located at `address 1`.

Firstly, the size of the array needs to be set to the maximum length:
`2 ^ 256 - 1`. Each item in the array is located at `keccak256(&arr.length) +
index`. Therefore to set the value of `flag` to `1` the following equation
needs to be satisfied:

```
keccak256(&arr.length) + index ≡ 1 (mod 2 ^ 256)
```

which becomes...

```
index ≡  1 - keccak256(&arr.length) (mod 2 ^ 256)
```

Finally, to get the flag run `python3 printFlag.py $index`.

### Walkthrough

#### 1. What is a .sol File?

When dealing with code that you've never seen before it's a good idea to Google
what it is...

> https://www.google.com/search?q=How+to+execute+a+.sol+file

The above URL leads us to the following article on `ethereum.stackexchange.com`

> https://ethereum.stackexchange.com/questions/3645/how-to-compile-sol-file-from-the-command-line

Some reading leads us to believe this is some Solidity source code.

And some reading from the [Solidity](https://en.wikipedia.org/wiki/Solidity)
Wikipedia article

> Solidity is an object-oriented programming language for writing smart
> contracts. It is used for implementing smart contracts on various blockchain
> platforms, most notably, Ethereum

> Solidity is a statically-typed programming language designed for developing
> smart contracts that run on the Ethereum Virtual Machine ...

#### 2. Understanding Remix

It would be great to execute (and debug) this .sol file but installing an IDE,
compiler, and debugger is for nerds.

After searching for "ethereum ide" on Google,
[Remix](https://remix.ethereum.org/) is first result. Remix is an IDE,
compiler, and debugger all in one web app :D

By clicking on the "Open File" link in [Remix](https://remix.ethereum.org/)
we can add a new file. Once the file has been added the "File Explorer" on the
left should show the file.

The contract can be compiled by clicking on the "Solidity Compiler" icon on the
left hand side of the panel. The "Compile vuln.sol" button can be used to
compile the contract which will allow us to run and debug the contract.

After the contract has been compiled the "Deploy & run transactions" icon on
the left hand side can be used to invoke the functions in the contract.

Click "Deploy" then at the bottom of the panel there should an entry for each
of the three functions (`setArrayLen()`, `setArrayValue()`, and `getFlag()`).
Once a function has been called there should be a button on the bottom right
hand side of the screen that says "Debug" which can be used to used to view
the contents of the storage (which we'll be using shortly).

#### 3. Where Do We Go From Here?

After playing around with the contract for a while it can be seen that the
`setArrayLen()` function actually sets the length of the array. This can be
confirmed by inserting values into the array using the `setArrayValue()`
function before and after calling the `setArrayLen()` function.

Hopefully you're comfortable with the Remix IDE and how to call functions. Now
lets get hacking :D

It's difficult to know where to go from here. One question you might ask is
"how does the setArrayLen() function work?". By answering this question we
might be one step closer to solving this challenge.

#### 4. How Does Solidity Store Data In Memory?

Well we know that variables need to be stored in memory, that's just a fact of
life. The length of an array is also a variable which must be stored in memory
somewhere. Where is the length stored though?

By trawling though the depths of the internet for the answer, you may find the
following article:

> https://programtheblockchain.com/posts/2018/03/09/understanding-ethereum-smart-contract-storage/

Without boring you with all the details of the article, here are some key
takeaways:
- The Ethereum Virtual Machine's address space contains 2^256 values.
- Each value is 32 bytes long (256 bits).
- Fixed sized variables are placed in storage in the order of deceleration.
- An array's length needs to be stored in memory and is also a fixed size
  variable.
- The location of `arr[i]` in memory is `keccak256(&arr.length) + i`.

Therefore, we can deduce the location of the objects declared in the given
contract:

| Address            | Variable     |
|--------------------|--------------|
| `0`                | `arr.length` |
| `1`                | `flag`       |
| `...`              | `...`        |
| `keccak256(0)`     | `arr[0]`     |
| `keccak256(0) + 1` | `arr[1]`     |
| `keccak256(0) + 2` | `arr[2]`     |
| `keccak256(0) + 3` | `arr[3]`     |

#### 5. `setArrayLen()` Internals

In the previous section we asked "how does the setArrayLen() function work?".
Now that we know how data is stored in memory it would be good to know what the
`sstore(0, len)` line does. After asking the oracle (aka Google) for some of
it's knowledge it tells us that the instruction evaluates to `storage[0] =
len`.

Well what's at address `0`? It's `arr.length`! Since we can write any value we
want, we control the length of the array.

#### 6. Calculating The Offset To `flag`

Now that we are Solidity experts, how can we actually change the value of
`flag`?

Using our ability to set the length of the array to any length we like, we can
set it to `2^256 - 1` to cover the entire address space of the EVM! After that,
we just need to find the right _index_ inside of the array to write to the
`flag` variable.

Since each address is only 256 bits long, any integer longer than 256 bits will
wrap around the address space. Therefore if we can find the _index_ with the
following equation then we'll be able to overwrite the flag.

```
keccak256(&arr.length) + index ≡ 1 (mod 2 ^ 256)
```

Then solve for _index_...

```
index ≡ 1 - keccak256(&arr.length) (mod 2 ^ 256)
```

Substitute `&arr.length` for `0`...

```

index ≡ 1 - keccak256(0) (mod 2 ^ 256)
```

Visiting the URL below is the quickest way of calculating `keccak256(0)` I can
think of:

> https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')Keccak('256')&input=MDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDAgMDA

Our equation is now:

```
index ≡ 1 - 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563 (mod 2 ^ 256)
```

Using some python magic ...

```bash
$ python3
Python 3.9.5 (default, May 11 2021, 08:20:37)
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> (1 - 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563) % (2**256)
97222658762210312835982718871080339316596872691747246639997364149093866936990
```

In summary,
`arr[97222658762210312835982718871080339316596872691747246639997364149093866936990]`
is located address `1` which is also the address of `flag`!

#### 7. Writing To `flag`

To test our hypothesis we can call the `setArrayLen()` function with
`len = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff`.
After that, call `setArrayValue()` with
`key = 97222658762210312835982718871080339316596872691747246639997364149093866936990`.
Finally, call `getFlag()` to see that `1` is returned :D

#### 8. Printing the Flag

```bash
$ python3 printFlag.py 97222658762210312835982718871080339316596872691747246639997364149093866936990
b'SKYLIGHT{TH!S_w0uld_HaVe_be3n_A_lot_3asIer_1n_C}'
```

### Flag

```
SKYLIGHT{TH!S_w0uld_HaVe_be3n_A_lot_3asIer_1n_C}
```

</details>
