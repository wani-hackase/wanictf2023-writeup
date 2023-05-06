---
title: fermat
level: 2
flag: FLAG{you_need_a_lot_of_time_and_effort_to_solve_reversing_208b47bd66c2cd8}
writer: Laika
---

# fermat

## 問題文

Give me a counter-example

## 解法

GDBなどのデバッガでprint_flagへジャンプさせる動的解析や、Ghidraなどのデコンパイラを利用してフラグを出力する箇所を解析し再現する静的解析など、様々な解き方があります。
また、a, b, cはuint32_t型であり、この型が扱える整数の範囲で $a^3 + b^3 = c^3$ が成立するような入力も存在します。

______________________________________________________________________

There exist various methods to tackle this problem, such as dynamic analysis, which involves jumping to print_flag using debuggers like GDB, or static analysis, which involves analyzing and replicating the locations that output the flags using decompilers like Ghidra.

Furthermore, there exist inputs where a, b, and c are of type uint32_t, and the equation $a^3 + b^3 = c^3$ holds true within the range of integers that can be handled by this type.
