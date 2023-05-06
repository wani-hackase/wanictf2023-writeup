---
title: "Just_Passw0rd"
level: 1
flag: "FLAG{1234_P@ssw0rd_admin_toor_qwerty}"
writer: "Mikka"
strings: false
---

## 問題文

ELFファイルはWSLやLinux等で`./just_password`と入力することで実行できます。

この問題のELFファイルは実行するとパスワードの入力を求められますが、パスワードが分からなくても中身を覗き見る方法はありますか？

ELF file can be executed by typing `./just_password` in WSL or Linux.

In this challenge, The ELF file requires password. Is there a way to look inside without knowing the password?

## 解法

stringsコマンドを使用すると、ファイルの中の文字列が出てくる。

```
strings just_password
```

その他、デコンパイラやバイナリエディタで中を覗くなどの方法がある。

When you use `strings` command, you will see the strings inside the file.

You can also use a decompiler or a binary editor to look inside the file.
