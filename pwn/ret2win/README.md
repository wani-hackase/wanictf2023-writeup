---
title: 03. ret2win
level: 2
flag: FLAG{f1r57_5739_45_4_9wn3r}
writer: Caffeine
badge: true
---

# 03. ret2win

## 問題文

プログラム内で新たに関数が呼ばれると、現在実行している命令へのポインタは一時的にスタック領域に保存されます。
スタック領域に退避した命令ポインタ(通称: リターンアドレス)を関数実行後に復元することで、関数を呼んだ直後からプログラムを継続することができます。

もし仮にリターンアドレスを書き換えることができれば、あなたはプログラム内の自由なアドレスにジャンプして命令を実行することができます。

main関数終了後に復元されるリターンアドレスをwin関数のアドレスに書き換えることで、シェルを取ることができるでしょうか？

`nc ret2win-pwn.wanictf.org 9003`

______________________________________________________________________

When a new function is called in a program, the pointer to the currently executing instruction is temporarily stored in the stack area.
By restoring the instruction pointer, also known as the return address, that was saved in the stack area after the function call, the program can continue execution from where it left off immediately after the function call.

If you were able to overwrite the return address, you could jump to a free address in the program and execute instructions there.
Could you take control of the shell by overwriting the return address that is restored after the main function ends with the address of the win function?

`nc ret2win-pwn.wanictf.org 9003`

## 解法

[English ver.](#eng)

Buffer Overflowでmain関数のリターンアドレスをwin関数のアドレスに書き換える。

具体的な説明をする前に、ここから先のpwnカテゴリの問題を解くためにもLinux環境上に以下のツールをインストールすることを推奨します。

### objdump

オブジェクトファイルや実行ファイルを調査するためのコマンド。

```
$ sudo apt install binutils
```

### Python3

エクスプロイトコードを書く他、pipで便利なツールをインストールするためにもほぼ必須です。

```
$ sudo apt install python3
```

### pip

Pythonのパッケージをインストールするツール。
Python3をインストールした際に付属していなければインストールする。

```
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py
```

wgetがない場合は`sudo apt install wget`でインストールしてください。

### pwntools

CTFのpwnカテゴリを解くためにフレームワーク及びライブラリ。

```
$ pip install pwntools
```

ここから具体的な解法を説明する。

checksecでセキュリティ機構を確認すると以下の通り。

```
$ checksec chall

Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

PIEはposition-independent executableの略である。
これが無効(NO PIE)の場合は、実行ファイルの配置されるアドレスが固定化される。

win関数のアドレスは`objdump`などで確認すると0x401369であることが分かる。

```
0000000000401369 <win>:
$ objdump -D -j .text -M intel chall

                    .
                    .
0000000000401369 <win>:
  401369:       f3 0f 1e fa             endbr64
  40136d:       55                      push   rbp
  40136e:       48 89 e5                mov    rbp,rsp
  401371:       48 31 c0                xor    rax,rax
  401374:       48 31 f6                xor    rsi,rsi  
                    .
                    .
```

main関数からのリターンアドレスを0x401369に書き換えると、main関数が終了した後にwin関数が呼ばれてシェルを起動する。

本問では、`BUF_SIZE`が32であるのに対して`MAX_READ_LEN`が48である。
16バイト分オーバーフローしてスタックに書き込めることを利用して、リターンアドレスをwin関数のアドレスに書き換えられる。

エクスプロイトコードはsolverの中にあります。

______________________________________________________________________

<a name="eng"></a>

Using Buffer Overflow, you can overwrite the return address of the main function with the address of the win function.

Before providing a detailed explanation, it is recommended that you install the following tools on a Linux environment to solve pwn-category problems going forward.

### Python3

In addition to writing exploit code, it is almost essential to install useful tools with pip.

```
$ sudo apt install python3
```

### pip

A tool to install Python packages.
If it is not included when you install Python3, install it.

```
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py
```

If you do not have wget, install it with `sudo apt install wget`.

### pwntools

A framework and library to solve pwn-category problems.

```
$ pip install pwntools
```

Now let's delve into the specific steps to solve this challenge.

To check the security mechanisms used, we can use `checksec`.
Running it shows the following output:

```
$ checksec chall

Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

PIE stands for position-independent executable.
If it is disabled (NO PIE), the address at which the executable is loaded will be fixed.

The address of the win function can be determined by using `objdump` or other similar tools, which shows it to be 0x401369.

```
0000000000401369 <win>:
$ objdump -D -j .text -M intel chall

                    .
                    .
0000000000401369 <win>:
  401369:       f3 0f 1e fa             endbr64
  40136d:       55                      push   rbp
  40136e:       48 89 e5                mov    rbp,rsp
  401371:       48 31 c0                xor    rax,rax
  401374:       48 31 f6                xor    rsi,rsi  
                    .
                    .
```

By overwriting the return address of the main function with the address of the win function (0x401369), the win function is called after the main function exits, thus launching a shell.

In this challenge, although `BUF_SIZE` is 32, `MAX_READ_LEN` is 48.
By exploiting the fact that we can overflow 16 bytes and write to the stack, we can overwrite the return address with the address of the win function.

The exploit code can be found in the solver file.