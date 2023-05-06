import os
import random

ANSWER = list(range(10**4))
random.shuffle(ANSWER)
CHANCE = 15


def peep():
    global CHANCE
    if CHANCE <= 0:
        print("You ran out of CHANCE. Bye!")
        exit(1)
    CHANCE -= 1

    index = map(int, input("Index (space-separated)> ").split(" "))
    result = [ANSWER[i] for i in index]
    random.shuffle(result)

    return result


def guess():
    guess = input("Guess the numbers> ").split(" ")
    guess = list(map(int, guess))
    if guess == ANSWER:
        flag = os.getenv("FLAG", "FAKE{REDACTED}")
        print(flag)
    else:
        print("Incorrect")


def main():
    menu = """
    1: peep
    2: guess""".strip()
    while True:
        choice = int(input("> "))
        if choice == 1:
            result = peep()
            print(result)
        elif choice == 2:
            guess()
        else:
            print("Invalid choice")
            break
