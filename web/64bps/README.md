---
title: 64bps
level: 2
flag: FLAG{m@ke_use_0f_r@n0e_reques7s_f0r_l@r9e_f1les}
writer: ciffelia
badge: true
---

# 64bps

## 問題文

```sh
dd if=/dev/random of=2gb.txt bs=1M count=2048
cat flag.txt >> 2gb.txt
rm flag.txt
```

↓↓↓

<https://64bps-web.wanictf.org/2gb.txt>

## 解法

English follows Japanese.

問題文にはUnixのコマンドが記載されており、これには次のような意味があります。

```sh
# 2gb.txtを作成し、2GiB (2147483648 bytes) のランダムなデータを書き込む
dd if=/dev/random of=2gb.txt bs=1M count=2048

# flag.txtの内容を2gb.txtの末尾に追記する
cat flag.txt >> 2gb.txt

# flag.txtを削除する
rm flag.txt
```

つまり`2gb.txt`の先頭2GiBはランダムなデータで、末尾にフラグがあることがわかります。

さて、問題文に記載されたリンクから`2gb.txt`を開こうとすると、ページが読み込み中のまま動かないはずです。問題のzipファイルをダウンロードしてみると`nginx.conf`に次のような記述があり、サーバーは1接続あたり64bpsの速度でしかダウンロードさせてくれないことがわかります。

```
limit_rate         8; # 8 bytes/s = 64 bps
```

2GiBのファイルを先頭からダウンロードしていたら末尾に辿り着くまで10年かかってしまい、WaniCTFの終了時間にはとても間に合いません。

そこで活用するのがHTTPの`Range`ヘッダーです。このヘッダーを使うと、巨大なレスポンスの中から好きな部分だけをダウンロードすることができます。

[HTTP 範囲リクエスト - HTTP | MDN](https://developer.mozilla.org/ja/docs/Web/HTTP/Range_requests)

今回はファイルの`2147483648`バイト目以降がほしいので、次のようにcurlを使うとフラグが手に入ります。

```sh
curl --verbose --header 'Range: bytes=2147483648-' https://64bps-web.wanictf.org/2gb.txt

# 次のように書いても同じです
curl --verbose --range '2147483648-' https://64bps-web.wanictf.org/2gb.txt
```

---

The challenge statement contains a Unix command, which means the following.

```sh
# Create 2gb.txt and write 2 GiB (2147483648 bytes) of random data
dd if=/dev/random of=2gb.txt bs=1M count=2048

# Append the contents of flag.txt to the end of 2gb.txt
cat flag.txt >> 2gb.txt

# Delete flag.txt
rm flag.txt
```

So we can see that the first 2 GiB of `2gb.txt` is random data and the flag is at the end.

Now, if you try to open `2gb.txt` from the link provided in the statement, the page should stay stuck while loading. If you download the zip file in question, you will see the following statement in `nginx.conf`, indicating that the server will only let you download at a speed of 64 bps per connection.

```
limit_rate         8; # 8 bytes/s = 64 bps
```

If you try to download a 2 GiB file from the beginning, it would take 10 years to reach the end, and you would never make it to the end of WaniCTF in time.

This is where the `Range` header of HTTP comes into play. With this header, you can download just any part of a huge response.

[HTTP range requests - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)

In this case, we want the `2147483648`th byte of the file and beyond, so we can get the flag by using curl as follows.

```sh
curl --verbose --header 'Range: bytes=2147483648-' https://64bps-web.wanictf.org/2gb.txt

# The same can be written as follows
curl --verbose --range '2147483648-' https://64bps-web.wanictf.org/2gb.txt
```
