from pwn import *
import sys

# io = process('chall')
io = remote("netcat-pwn.wanictf.org", 9001)

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]

cnt = 0

while True:
    r = io.recvuntil(b" + ")
    a = int(r[-6:-3].decode())
    r = io.recvuntil(b" = ")
    b = int(r[0:3].decode())
    print(f"{a} + {b} = {a + b}")
    io.sendline(str(a + b).encode())
    r = io.recvline()
    print(r)
    if r == b"Cool!\n":
        cnt += 1
    if cnt >= 3:
        break

io.interactive()
