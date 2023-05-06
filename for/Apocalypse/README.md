---
title: "Apocalypse"
level: 4
flag: "FLAG{Watch_out_4_2023_21036}"
writer: "Mikka"
---

# Apocalypse

## 問題文

ファイルが切り取られてしまったみたいです。

※フラグ形式は`FLAG{[0-9a-zA-Z_]+}`です。


It looks like the file has been cut off.

*The flag format is `FLAG{[0-9a-zA-Z_]+}`.

## 解法

PNGが中途半端に切断されているので、読み込まれていないデータがあると予想できる。

IEND(PNGファイルの終わりを示すチャンクの文字)をバイナリエディタで検索すると2つあるので、最初にある方のIENDを削除(適当な文字列で置き換え)する。

そうするとファイルの最後のIENDだけが有効になるのでデータ全体が読み込まれるようになり、文字列が出現する。

文字列の一部がまだ見えない場合は、IENDを置き換えた文字列をさらに適当なものに変更することで文字列が移動する。

※綺麗には復元できないためアンダースコア`_`が見えにくく、文字の間隔と問題文から推測する必要がありました。

The PNG is cut off in the middle, so you can expect that some data has not been loaded.

Look up the IEND (characters that marks the end of the PNG file) in a binary editor and you will find two IENDs.

If you replace the first one with some random binary, the last one in the file will be valid, so entire data will be read and the FLAG will appear.

If the FLAG is still not visible, it can be moved by changing the binary that replaced the IEND.

*The underscore`_` was difficult to see because it could not be recovered cleanly and had to be inferred from the spacing of the characters and the challenge statement.