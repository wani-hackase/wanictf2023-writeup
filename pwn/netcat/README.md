---
title: 01. netcat
level: 1
flag: FLAG{1375_k339_17_u9_4nd_m0v3_0n_2_7h3_n3x7!}
writer: Caffeine
badge: true
---

# 01. netcat

## 問題文

Pwnable(pwn)の世界へようこそ！

pwnカテゴリでは、netcat(nc)と呼ばれるコマンドラインツールを利用して問題サーバとやり取りを行う形式が一般的です。
コマンドラインから `nc <接続先ホストのURL> <ポート番号>`と入力すると、通信を待ち受けているサーバにアクセスできます。

以下のコマンドを入力して、問題サーバとデータの送受信が確立されていることを確認してみましょう。

`nc netcat-pwn.wanictf.org 9001`

### ヒント

- まずは表示される計算問題に挑戦しましょう
- 計算問題をクリアしたら新たにシェルが起動します。画面に何も表示されなくとも慌てる必要はありません。試しに知っているコマンド(`ls`や `cat`など)を入力してみましょう。

______________________________________________________________________

In the pwn category, it is common to interact with the problem server using a command-line tool called netcat (nc).
By entering `nc <host> <port number>` from the command line, you can access the server that is waiting for communication.

Enter the following command to confirm that the problem server and data transmission have been established.

`nc netcat-pwn.wanictf.org 9001`

### Hint

- First, let's challenge the displayed arithmetic problem.
- After clearing the arithmetic problem, a new shell will be launched. There is no need to panic even if nothing is displayed on the screen. Try entering a command you know (such as `ls` or `cat`).

## 解法

[English ver.](#eng)

コマンドラインから`nc netcat-pwn.wanictf.org 9001`を入力すると以下のような画面が表示される。

```
+-----------------------------------------+
| your score: 0, remaining 100 challenges |
+-----------------------------------------+

465 + 998 =
```

最大100問出題される計算問題に3問連続で正解すればシェルが起動する。

シェルが起動したら、`cat FLAG`を入力する。
(`cat`はファイルの中身を表示するコマンドです。)

ファイル名は`ls`コマンドなどで確認できます。

______________________________________________________________________

<a name="eng"></a>

Upon entering `nc netcat-pwn.wanictf.org 9001` in the command line, it will be displayed as follow:

```
+-----------------------------------------+
| your score: 0, remaining 100 challenges |
+-----------------------------------------+

465 + 998 =
```

If you correctly answer three consecutive calculation problems out of a maximum of 100 questions, the shell will be launched.

Once the shell is launched, enter `cat FLAG` to display the flag.
(`cat` is a command that displays the contents of a file.)

You can confirm the file name by using commands such as `ls`.