---
title: 02. only once
level: 1
flag: FLAG{y0u_4r3_600d_47_c41cu14710n5!}
writer: Caffeine
badge: true
---

# 02. only once

## 問題文

計算問題に3問連続正解したら、ご褒美にシェルをプレゼント！

あれ？1問しか出題されないぞ！？

`nc only-once-pwn.wanictf.org 9002`

### ヒント

- pwnカテゴリでは、問題サーバで動いている実行ファイルとそのソースコードが配布されていることが多いです。"netcat"のソースコードと比較してどこが変化しているでしょうか。

______________________________________________________________________

If you provide three consecutive correct answers to a math problem, you will be rewarded with a shell!

Oh, wait, it seems like only one question is being asked!?

`nc only-once-pwn.wanictf.org 9002`

### Hint

- In the pwn category, it is common for the problem server to distribute executable files and their source code. How does it differ from the source code of "netcat"?

## 解法

[English ver.](#eng)

Buffer Overflowで局所変数を書き換える。

問題サーバに接続すると、以下のような画面が表示される。

```
+---------------------------------------+
| your score: 0, remaining 1 challenges |
+---------------------------------------+

662 + 359 =
```

シェルを起動するためには少なくとも3つの計算問題に挑戦する必要があるが、最初から残り問題数が1つしかない。
どうしたものか...

本問では、`buf`を最大8バイトの文字配列として宣言して `scanf("%8s", buf)`している。
その後 `atoi(buf)`で入力文字列を整数型として解釈する。

一見すると問題なさそうに見えるが、実際の `scanf("%8s", buf)`の動作は**改行が入力されるまで最大8バイトの文字入力を受け付けた後にNULL終端を行う**というもの。
改行を除いて8バイト以上の入力を与えるとNULL文字がbufの境界を破って書き込まれてしまう (いわゆるoff-by-one-null error)。

`scanf`をcallする直前のスタックは以下のような状態になっている。

```
      +---------------+ <- rsp
+0x00 |    (blank)    |
      +---------------+
+0x08 |      buf      |
      +---------------+
+0x10 | score | chall |
      +---------------+
+0x18 |   x   |   y   |
      +---------------+
  :
```

Off-by-one-null errorが生じると変数 `chall`の最下位バイトが `0x00`に書き換えらる。

`chall`は残り挑戦回数を格納するint型の変数で、1 (0x00000001)で初期化される。
最下位バイトを0x00に書き換えると0 (0x00000000)になる。

`chall`はwhileループの最後にデクリメントされて0から-1 (0xffffffff)になる。
ループをbreakする条件が `chall == 0`なので，これにて2問目以降の問題が出題されるようになる。

______________________________________________________________________

<a name="eng"></a>

Exploiting buffer overflow to overwrite local variables.

Upon connecting to the problem server, it will be displayed as follow:

```
+---------------------------------------+
| your score: 0, remaining 1 challenges |
+---------------------------------------+

662 + 359 =
```

To launch the shell, you need to attempt at least three calculation problems, but there seems to be only one question remaining from the start.
What should you do...

In this problem, `buf` is declared as a character array of up to 8 bytes and then scanned with `scanf("%8s", buf)`.
The input string is then interpreted as an integer type with `atoi(buf)`.

At first glance, there seems to be no problem, but the actual behavior of `scanf("%8s", buf)` is **to accept up to 8 bytes of input until a newline character is entered, then terminate with a NULL character**.
If an input of 8 or more bytes excluding the newline character is given, a NULL character will be written beyond the boundary of `buf`, causing an off-by-one-null error.

The stack before calling scanf is in the following state.

```
      +---------------+ <- rsp
+0x00 |    (blank)    |
      +---------------+
+0x08 |      buf      |
      +---------------+
+0x10 | score | chall |
      +---------------+
+0x18 |   x   |   y   |
      +---------------+
  :
```

An off-by-one-null error will overwrite the lowest byte of the variable `chall` with 0x00.

`chall` is an integer variable that stores the number of remaining attempts and is initialized to 1 (0x00000001). 
Overwriting the lowest byte with 0x00 will result in it becoming 0 (0x00000000).

`chall` is decremented at the end of the while loop and becomes -1 (0xffffffff).
The loop is exited when `chall == 0`, which enables the second and subsequent problems to be presented.