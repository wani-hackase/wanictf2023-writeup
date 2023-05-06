---
title: 05. beginners ROP
level: 3
flag: FLAG{h0p_p0p_r0p_po909090p93r!!!!}
writer: Caffeine
badge: true
---

# 05. beginners ROP

## 問題文

"ret2win"では、リターンアドレスをwin関数のアドレスに書き換えることでシェルを取りました。

本問ではwin関数がありません。このような場合、return-oriented programming (ROP)という攻撃手法が有効です。gadgetと呼ばれるretで終了する命令の断片を連続的に呼び出すことで、シェルを起動してください。

`nc beginners-rop-pwn.wanictf.org 9005`

______________________________________________________________________

In "ret2win," the shell was obtained by overwriting the return address with the address of the win function.

In this challenge, there is no win function available. In such cases, return-oriented programming (ROP) is an effective attack technique. You can launch a shell by continuously calling fragments of instructions that end with a "ret" called gadgets.

`nc beginners-rop-pwn.wanictf.org 9005`

## 解法

[English ver.](#eng)

Buffer OverflowでROPを組んで `execv("/bin/sh", 0, 0)`を成立させてシェルを起動する。

問題文に記載されているように、retで終了する命令を連続的に呼び出すことでレジスタやメモリを操作することが可能です。

過去のWaniCTFの作問者writeupに詳しい説明があるので、ROPを学びたい方は是非[こちら](https://github.com/wani-hackase/wanictf2020-writeup/tree/master/pwn/06-rop-func-call)をご覧ください。

本問には、`pop rax; ret`や`xor rsi, rsi; ret`などの有用なガジェットが意図的に仕込まれているので有難く利用しましょう。

エクスプロイトコードはsolverの中にあります。

______________________________________________________________________

<a name="eng"></a>

By constructing a ROP chain, you can successfully execute `execv("/bin/sh", 0, 0)`, thereby launching a shell.

As mentioned in the problem statement, we can manipulate registers and memory by calling a sequence of instructions that end with a ret instruction.

For those who want to learn ROP, there is a detailed explanation in [author's writeup of the past WaniCTF](https://github.com/wani-hackase/wanictf2020-writeup/tree/master/pwn/06-rop-func-call).
(As Japanese explanations are included, please make good use of the translation function :D)

This problem intentionally includes useful gadgets such as `pop rax; ret` and `xor rsi, rsi; ret`, so let us gratefully utilize them.

The exploit code can be found in the solver file.