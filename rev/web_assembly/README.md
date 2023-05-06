---
title: web_assembly
level: 4
flag: Flag{Y0u_C4n_3x3cut3_Cpp_0n_Br0us3r!}
writer: kaki005
badge: true
---

# 問題名

web_assembly

## 問題文

ブラウザ上でC++を動かすことに成功しました！！ 正しいユーザ名とパスワードを入力するとフラグがゲットできます。

I successfully ran C++ in the browser!! Enter the correct username and password to get the flag.

<https://wasm-rev.wanictf.org>

---

注意: 作問におけるミスにより、フラグは`Flag{`から始まり`}`で終わります。ご迷惑をおかけして申し訳ありません。

Note: This flag starts `Flag{` and ends `}`. Sorry for the inconvenience.

## 解法

1. ブラウザの開発者ツールからindex.wasmをダウンロードできます。
2. ghidraでwasm用のプラグイン(https://github.com/nneonneo/ghidra-wasm-plugin)を導入します。
3. wasmファイルをghidraで解析するとmain関数を見つけます。
   If you analyze the wasm file with ghidra, you will find the main function
4. main関数でパスワードとユーザ名を検証しているので、正しいユーザ名(ckwajea)とパスワード(feag5gwea1411_efae!!)を発見できます。
5. サイト上で正しいユーザ名とパスワードを入力することでフラグが表示されます。




---
1. You can download index.wasm from your browser's developer tools.
2. Install the plugin (https://github.com/nneonneo/ghidra-wasm-plugin) for wasm in ghidra.
3. If you analyze the wasm file with ghidra, you will find the main function
4. Since the password and username are verified in the main function, the correct username (ckwajea) and password (feag5gwea1411_efae!!) can be found.
5. Enter the correct username and password on the site and the flag will appear.
