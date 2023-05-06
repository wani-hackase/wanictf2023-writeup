---
title: "theseus"
level: 3
flag: "FLAG{vKCsq3jl4j_Y0uMade1t}"
writer: "Mikka"
---

## 問題文

FLAGと同じ文字列を打ち込むと`Correct!`と表示されます。


Input the same strings as FLAG and you'll get the 'Correct!'.

## 解法

静的解析(例：Ghidra)などで、compare関数のアセンブリコードに足し算をする処理があることが分かる。

足し算で参照され書き換えられている部分を見ると、事前に格納された定数(文字列)が改変されている。

プログラムとアセンブリコードを読んで、足し算をする処理を再現すればいい。


Static analysis (like Ghidra) shows that there is some add operation in the assembly code of the 'compare' function.

By examining the part that is referenced and rewritten by the addition, you can see that strings has been modified.

Recreate the process of addition by reading the assembly code and you'll get the FLAG.
