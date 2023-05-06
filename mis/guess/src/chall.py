import os
import random

ANSWER = list(range(10**4))
CHANCE = 15
OPTIONS = """
1: peep
2: guess
> """

random.shuffle(ANSWER)


def peep():
    global CHANCE
    if CHANCE <= 0:
        print("You ran out of CHANCE. Bye!")
        return
    CHANCE -= 1

    index = input("index> ").split()
    index = map(int, index)

    output = [ANSWER[i] for i in index]
    random.shuffle(output)
    print(output)


def guess():
    guess = input("Guess the list> ").split()
    guess = list(map(int, guess))

    if guess == ANSWER:
        flag = os.getenv("FLAG", "FAKE{REDACTED}")
        print(flag)
    else:
        print("Incorrect!")


while True:
    choice = input(OPTIONS)
    choice = int(choice)

    if choice == 1:
        peep()
    elif choice == 2:
        guess()
    else:
        print("Invalid choice!")
        break
