---
title: certified1
level: 3
flag: FLAG{7he_sec0nd_f1a9_1s_w41t1n9_f0r_y0u!}
writer: ciffelia
badge: true
---

# certified1

## 問題文

最近流行りの言語を使った安全なウェブアプリが完成しました！

We have released a secure web application using a state-of-the-art language!

<https://certified-web.wanictf.org>

---

この問題にはフラグが2つ存在します。ファイル`/flag_A`にあるフラグをcertified1に、環境変数`FLAG_B`にあるフラグをcertified2に提出してください。

There are two flags in this problem. Please submit the flag in file `/flag_A` to certified1 and one in the environment variable `FLAG_B` to certified2.

Note: "承認, ワニ博士" means "Approved, Dr. Wani" in Japanese.

## 解法

English follows Japanese.

まずはアプリケーションの概要を確認します。

- 画像をアップロードすると、「承認」と書かれたはんこの画像を合成して表示するアプリです。
- 画像は `multipart/form-data` 形式のPOSTリクエストでアップロードします。
- バックエンドはRustで実装されており、画像の合成処理にはImageMagick 7.1.0-51を使っています。

ImageMagickは脆弱性が頻繁に発見されるアプリケーションとして知られています。この問題ではImageMagick 7.1.0-51が使われているため、それ以降のバージョンで修正された脆弱性が存在しないか調べるとCVE-2022-44267とCVE-2022-44268が見つかります。

- [画像処理ソフト「ImageMagick」に脆弱性、情報漏洩の恐れ | TECH+（テックプラス）](https://news.mynavi.jp/techplus/article/20230203-2582052/)
- [ImageMagick: The hidden vulnerability behind your online images - Metabase Q](https://www.metabaseq.com/imagemagick-zero-days/)

CVE-2022-44267とCVE-2022-44268はどちらもImageMagickのPNGパーサーのバグに起因します。細工されたPNG画像を読み込ませたとき、ImageMagickがフリーズするのがCVE-2022-44267、出力のPNG画像にサーバー上の任意のファイルの内容が含まれてしまうのがCVE-2022-44268です。これらは7.1.0-52で修正されており、この問題ではCVE-2022-44268が使えそうであることがわかります。

Metabase Qの記事を参考にしつつ、GitHubで公開されているPoCを使って攻撃を行ってみましょう。Rust, ImageMagick, Pythonが必要です。

https://github.com/voidz0r/CVE-2022-44268

上記のリポジトリをクローンし、READMEとソースコードを確認してください。`cargo run '/flag_A'`を実行すると、カレントディレクトリに`image.png`が生成されます。これをhankoにアップロードして、表示されたPNG画像をダウンロードします。

ダウンロードしたPNG画像を`magick identify -verbose <ファイル名>`で解析すると、`Raw profile type:`の部分に16進数表記の文字列が含まれていることがわかります。このHEX文字列から改行を除去し、Pythonで`bytes.fromhex()`を使ってデコードすると1つ目のフラグが手に入ります。

なお、セキュリティVTuberのkurenaifさんが動画でこの脆弱性について解説されています。詳しく知りたい方はあわせてご覧ください。動画で扱われている内容にはcertified2の部分的なネタバレが含まれていますのでご注意ください。

[【ImageMagick】ImageMagickであった情報漏洩の脆弱性を詳しく解説！【cve-2022-44268】【悪用厳禁】 - YouTube](https://www.youtube.com/watch?v=KbCR_lkVU5w)

---

First, let's review the application overview.

- When an image is uploaded, this application composites and displays an image. The image is composited with a stamp with the word "Approval".
- The image is uploaded as a POST request in `multipart/form-data` format.
- The backend is implemented in Rust and uses ImageMagick 7.1.0-51 for the image composition.

ImageMagick is known as an application for which vulnerabilities are frequently discovered. Since ImageMagick 7.1.0-51 is used in this issue, CVE-2022-44267 and CVE-2022-44268 can be found by checking for the existence of vulnerabilities fixed in later versions.

[ImageMagick: The hidden vulnerability behind your online images - Metabase Q](https://www.metabaseq.com/imagemagick-zero-days/)

Both CVE-2022-44267 and CVE-2022-44268 result from a bug in ImageMagick's PNG parser. CVE-2022-44267 causes ImageMagick to freeze when loading crafted PNG images, and CVE-2022-44268 causes the output PNG image to contain the contents of an arbitrary file on the server. These vulnerabilities have been fixed in 7.1.0-52, indicating that CVE-2022-44268 may be used for this issue.

Using the Metabase Q article as a guide, let's try to perform the attack using the PoC available on GitHub. Rust, ImageMagick, and Python are required.

https://github.com/voidz0r/CVE-2022-44268

Clone the above repository and check the README and source code. Run `cargo run '/flag_A'`, which will generate `image.png` in the current directory. Upload this to hanko and download the displayed PNG image.

Analyze the downloaded PNG image with `magick identify -verbose <file name>` and you will see that the `Raw profile type:` contains a string in hexadecimal notation. If you remove the newlines from this hex string and decode it in Python using `bytes.fromhex()`, you will get the first flag.
