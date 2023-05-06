---
title: "javersing"
level: 2
flag: "FLAG{Decompiling_java_is_easy}"
writer: "Mikka"
---

## 問題文

jarファイルの中身を覗いてみましょう！


Let's take a look at the contents of .jar file!

## 解法

適当なjavaのデコンパイラにjarファイルを突っ込む。
オンラインのものの例：http://www.javadecompilers.com/

jarファイルはjavaのソースコードにほぼ完全な形で復元できる。

後は処理を読んで、data文字列を並び替えるプログラム(javaのソースコードと同じもの)を任意の言語で再現し、手元で出力すればよい。


Put the jar file into a random java decompiler. (e.g.http://www.javadecompilers.com/)

You can almost completely restore the jar file to the java source code.

Afterwards, you can read the process, write a program that does the same thing in your favorite language, and output FLAG.