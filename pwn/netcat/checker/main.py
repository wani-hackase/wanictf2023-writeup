from pwn import *
import sys


def pwn_netcat(host):
    try:
        io = remote(host, 9001, timeout=3)
    except Exception:
        return 2

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
    if b"FLAG{1375_k339_17_u9_4nd_m0v3_0n_2_7h3_n3x7!}" in r:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if pwn_netcat(sys.argv[1]) != 0:
        exit(1)
