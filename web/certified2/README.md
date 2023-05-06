---
title: certified2
level: 5
flag: FLAG{n0w_7hat_y0u_h4ve_7he_sec0nd_f1a9_y0u_4re_a_cert1f1ed_h4nk0_m@ster}
writer: ciffelia
badge: true
---

# certified2

## 問題文

certified1をご覧ください。

Please see certified1.

## 解法

English follows Japanese.

一般に、現在のプロセスが起動された際の環境変数は`/proc/self/environ`から読み出すことができます。しかしこの問題では、certified1と同様にCVE-2022-44267を使って`/proc/self/environ`を読み出そうとすると中身が空になってしまいます。

この現象の原因は、`/proc/self/environ`の見かけ上のファイルサイズが0バイトであることにあります。ImageMagickはファイルを読み込む際に`lseek(2)`を`SEEK_END`で呼び出し、得られたファイルサイズの分だけ`mmap(2)`を使って読み出します（ImageMagickのソースコードを読むか`strace`を使うとわかります）。procfsはこの操作に対してファイルサイズを0バイトと報告するため、ImageMagickはこのファイルの中身を読み出すことができません。

[linux - How does /proc/* work? - Super User](https://superuser.com/questions/619955)

さて、実はこのアプリケーションにはディレクトリトラバーサルの脆弱性があり、任意のファイルをImageMagickの入力用一時ファイル（Docker環境であれば`/data/<id>/input`）にコピーすることができます。これを組み合わせることで、`/proc/self/environ`の内容を`/data/<id>/input`にコピーし、CVE-2022-44267を使って内容を取得できます。

ディレクトリトラバーサルの脆弱性について詳しく見ていきましょう。`POST /create`を処理する`handle_create()`では、リクエストに対してランダムなIDを生成し、ユーザーから送信されたファイルを`./data/<id>/<filename>`に保存しています。ここではユーザーから送信されたファイル名をサニタイズしておりディレクトリトラバーサルを防いでいます。

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/handler/create.rs#L23-L32

次の行では、ユーザーから送信されたファイル名を`process_image()`に渡しています。

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/handler/create.rs#L34-L36

`process_image()`では、`./data/<id>/<filename>`を`./data/<id>/input`にコピーしています。ここでファイル名の扱いに問題があり、ユーザーから送信されたファイル名をサニタイズしていません。このため、例えば`/proc/self/environ`をファイル名として指定すると、その中身が`./data/<id>/input`にコピーされてしまいます。

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/process_image.rs#L8-L13

実際に攻撃を行うコードは次の通りです。ファイルは`multipart/form-data`で送信しているので、ファイル名は`Content-Disposition`ヘッダで指定します。

```python
import requests

origin = 'https://certified-web.wanictf.org'

res = requests.post(
    f"{origin}/create",
    headers={"content-type": 'multipart/form-data;boundary="boundary"'},
    data='--boundary\r\nContent-Disposition: form-data; name="file"; filename="/proc/self/environ"\r\nContent-Type: text/plain\r\n\r\n\r\n--boundary',
    timeout=3,
)

print(res.text) # ... image processing failed on ./data/<id>: ...
```

あとはcertified1と同様の手順で`/data/<id>/input`の中身を取得すれば2つ目のフラグが手に入ります。

---

In general, the environment variable with which the current process was started can be read from `/proc/self/environ`. However, in this issue, if you try to read `/proc/self/environ` using CVE-2022-44267 as well as certified1, the contents will be empty.

The cause of this phenomenon is that the apparent file size of `/proc/self/environ` is 0 bytes; ImageMagick calls `lseek(2)` with `SEEK_END` when reading the file and reads the resulting file size using `mmap(2)` (read the ImageMagick source code or use `strace` to find out). Since procfs reports the file size as 0 bytes for this operation, ImageMagick cannot read the contents of this file.

[linux - How does /proc/* work? - Super User](https://superuser.com/questions/619955)

Now, in fact, this application has a directory traversal vulnerability that allows arbitrary files to be copied into a temporary file for ImageMagick input (`/data/<id>/input` in a Docker environment). These vulnerabilities combined, the contents of `/proc/self/environ` can be copied to `/data/<id>/input` and the contents retrieved using CVE-2022-44267.

Let's take a closer look at the directory traversal vulnerability. In `handle_create()`, which handles `POST /create`, a random ID is generated for the request and the file sent by the user is copied to `./data/<id>/<filename>`. Here the filename submitted by the user is sanitized to prevent directory traversal.

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/handler/create.rs#L23-L32

The next line passes the filename submitted by the user to `process_image()`.

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/handler/create.rs#L34-L36

In `process_image()`, `./data/<id>/<filename>` is copied to `./data/<id>/input`. There is a problem here with filename handling, and the filename sent by the user is not sanitized. So, for example, if you specify `/proc/self/environ` as the filename, its content will be copied to `./data/<id>/input`.

https://github.com/wani-hackase/wanictf2023-writeup/blob/main/web/certified1/file/src/process_image.rs#L8-L13

The actual code for the attack is as follows. Since the file is sent as `multipart/form-data`, the file name is specified in the `Content-Disposition` header.

```python
import requests

origin = 'https://certified-web.wanictf.org'

res = requests.post(
    f"{origin}/create",
    headers={"content-type": 'multipart/form-data;boundary="boundary"'},
    data='--boundary\r\nContent-Disposition: form-data; name="file"; filename="/proc/self/environ"\r\nContent-Type: text/plain\r\n\r\n\r\n--boundary',
    timeout=3,
)

print(res.text) # ... image processing failed on ./data/<id>: ...
```

Now you can get the second flag by following the same procedure as certified1 to get the contents of `/data/<id>/input`.
