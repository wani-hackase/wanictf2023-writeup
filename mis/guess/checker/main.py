import ast
import sys

from pwn import *


def peep(_r, index: list[int]) -> list[int]:
    _r.sendlineafter(b"> ", b"1")
    _r.sendlineafter(b"> ", " ".join(map(str, index)).encode())

    result = ast.literal_eval(_r.recvline().decode().split(": ")[-1])

    return result


def guess(_r, value: list[int]):
    _r.sendlineafter(b"> ", b"2")
    _r.sendlineafter(b"> ", " ".join(map(str, value)).encode())


def mis_guess(host: str, port: int, timeout: int = 3):
    try:
        _r = remote(host, port, timeout=timeout)
    except Exception:
        return 2

    X = []
    for i in range(14):
        result = peep(_r, [x for x in range(10**4) if x >> i & 1])
        X.append(result)

    answer = [0] * (10**4)
    for num in range(10**4):
        pos = 0
        for bit, x in enumerate(X):
            pos |= int(num in x) << bit

        answer[pos] = num

    guess(_r, answer)
    flag = _r.recvline()
    if b"FLAG{How_did_you_know?_10794fcf171f8b2}" in flag:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if mis_guess(sys.argv[1], 50018) != 0:
        exit(1)
