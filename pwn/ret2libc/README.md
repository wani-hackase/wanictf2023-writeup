---
title: 07. ret2libc
level: 3
flag: FLAG{c0n6r475_0n_6r4du471n6_45_4_9wn_b361nn3r!}
writer: Caffeine
badge: true
---

# 07. ret2libc

## 問題文

バイナリ内のgadgetのみを使用してROPを組むのが困難な場合、Linuxの標準Cライブラリ(libc)内のgadgetや関数を利用することが効果的です。

`nc ret2libc-pwn.wanictf.org 9007`

### ヒント

- libc内のgadgetを利用するためには、libcがメモリ内のどのアドレス読み出された特定する必要があります。
- main関数からのリターンアドレスには、もともとlibc内のアドレスが入っています。このアドレスは実行毎に変化しますが、libc内の相対的なアドレスは不変です。

______________________________________________________________________

Using only gadgets inside a binary to build a ROP chain can be challenging, in such cases, utilizing gadgets and functions in the standard C library (libc) in Linux can be an effective solution.

`nc ret2libc-pwn.wanictf.org 9007`

### Hint

- To use gadgets in libc, you need to determine the location of libc in memory.
- The return address from the main function already contains an address from libc. Although this address changes each time the program is executed, the relative address of libc is constant.

## 解法

[English ver.](#eng)

ROPを組んで `system("/bin/sh")`を成立させてシェルを起動する。

本問では、レジスタを任意に調整できるgadgetが用意されていない。
代わりに、実行ファイルと一緒に配布されているlibcを利用する。

Address space layout randomization (ASLR)が有効化されているため、libcがメモリ内のどこに配置されるかは実行毎に変化するが、libc内の関数やシンボルの相対アドレスは一定である。
main関数はlibc内の関数(本問では`__libc_start_call_main`)から呼ばれる。
即ち書き換える以前のリターンアドレスを参照すればlibc内の任意のgadgetや関数のアドレスが計算できる。

例えば、スタックの初期状態が以下のとき、libcは0x7fcfa32a6000を先頭に読み出されていることが計算できる。

```
  #############################################
  #                stack state                #
  #############################################

                 hex           string
       +--------------------+----------+
 +0x00 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x08 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x10 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x18 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x20 | 0x0000000000000001 | ........ |
       +--------------------+----------+
 +0x28 | 0x00007fcfa32cfd90 | .....,.. | <- TARGET!!!
       +--------------------+----------+
```

エクスプロイトコードはsolverの中にあります。

______________________________________________________________________

<a name="eng"></a>

Construct a ROP chain to execute `system("/bin/sh")` and launch a shell.

In this challenge, there are no gadgets available to manipulate registers arbitrarily.
Instead, you can leverage the libc that is distributed with the executable file.

Due to the activation of Address Space Layout Randomization (ASLR), the location of libc in memory changes with each execution, but the relative addresses of functions and symbols within libc remain constant.
The main function is called from a function within libc (in this challenge, `__libc_start_call_main`).
Therefore, by referring to the original return address before it was overwritten, it is possible to calculate the address of any gadget or function within libc.

For example, if the initial state of the stack is as follows, it can be calculated that libc is loaded at 0x7fcfa32a6000.

```
  #############################################
  #                stack state                #
  #############################################

                 hex           string
       +--------------------+----------+
 +0x00 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x08 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x10 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x18 | 0x0000000000000000 | ........ |
       +--------------------+----------+
 +0x20 | 0x0000000000000001 | ........ |
       +--------------------+----------+
 +0x28 | 0x00007fcfa32cfd90 | .....,.. | <- TARGET!!!
       +--------------------+----------+
```

The exploit code can be found in the solver file.