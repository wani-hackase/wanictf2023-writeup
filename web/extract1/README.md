---
title: Extract Service 1
level: 2
flag: FLAG{ex7r4c7_1s_br0k3n_by_b4d_p4r4m3t3rs}
writer: hi120ki
badge: true
---

# Extract Service 1

## 問題文

ドキュメントファイルの要約サービスをリリースしました！配布ファイルの`sample`フォルダにお試し用のドキュメントファイルがあるのでぜひ使ってください。

サーバーの`/flag`ファイルには秘密の情報が書いてあるけど大丈夫だよね...? どんなHTTPリクエストが送信されるのか見てみよう！

We have released a summary service for document files! Please feel free to use the sample document file in the "sample" folder of the distribution file for trial purposes.

The secret information is written in the `/flag` file on the server, but it should be safe, right...? Let's see what kind of HTTP request is sent!

<https://extract1-web.wanictf.org>

## 解法

ファイルをアップロードするPOSTリクエストに含まれる`target`パラメーターはフロントエンドから`word/document.xml`といったパスで指定されている。

ファイルのアップロード後はドキュメントファイルをzipファイルとして解凍し、`target`パラメーターのファイルを取得する。

ここを`../../flag`とすることで`/flag`ファイルを取得することができる。

```
curl -X POST http://localhost:8080 -F "file=@sample/sample.docx" -F "target=../../flag"
```

---

The `target` parameter included in the POST request to upload the file is specified in the path such as `word/document.xml` from the front end.

After uploading the file, the document file is decompressed as a zip file, and the file specified in the `target` parameter is obtained.

By setting it to `../../flag` here, the `/flag` file can be obtained.

```
curl -X POST http://localhost:8080 -F "file=@sample/sample.docx" -F "target=../../flag"
```
