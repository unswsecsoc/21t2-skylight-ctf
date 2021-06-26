#!/usr/bin/python3

# Very heavily influenced by @lecafard's quick maths challenge.

import sys, signal, secrets, functools

print = functools.partial(print, flush=True)

def main():
    print("Welcome to Catletics!")
    print("Try this week's quiz.")
    print("Answer all questions correctly and you shall get a prize!")
    print("Get one wrong and you'll be killed, or worse... expelled!\n")

    print("Oh, and you have 10 seconds. Good luck!\n")

    try:
        arith_count = 5
        while arith_count > 0:
            num1 = secrets.randbelow(2**15)
            num2 = secrets.randbelow(2**14)
            op = ['+', '-', '*', '%'][secrets.randbelow(4)]

            if int(input(f'What is {num1} {op} {num2}? ')) == eval(f'{num1} {op} {num2}'):
                print('Correct!')
            else:
                raise Exception
            arith_count -= 1

        num1 = secrets.randbelow(2**7)
        if int(input(f"What is 0b{'{0:08b}'.format(num1)} in hexadecimal? "), 16) == num1:
            print("Correct!")
        else:
            raise Exception

        num1 = secrets.randbelow(2**7)
        if int(input(f"What is {hex(num1)} in decimal? ")) == num1:
            print("Correct!")
        else:
            raise Exception

        num1 = secrets.randbelow(2**16)
        if int(input(f"What is {hex(num1)} in octal? "), 8) == num1:
            print("Correct!")
        else:
            raise Exception
        
        num1 = secrets.randbelow(2**15)
        num2 = secrets.randbelow(2**14)
        if int(input(f"What is {hex(num1)} + 0b{'{0:08b}'.format(num2)} in octal? "), 8) == num1 + num2:
            print("Correct!")
        else:
            raise Exception

        num1 = secrets.randbelow(96) + 32
        if input(f"What's {hex(num1)} as an ASCII character? ") == chr(num1):
            print("Correct!")
        else:
            raise Exception
        print(r"SKYLIGHT{pWnT00L5_m4St3R_0r%sC0Tt_fL4nsburG}")
    except:
        print("Guess you'll have to try again 😈")

if __name__ == '__main__':
    def interrupted(signum, frame):
        print("\nTime's up! Off to detention in the dungeons!")
        sys.exit(1)
    signal.signal(signal.SIGALRM, interrupted)

    signal.alarm(10)
    main()
