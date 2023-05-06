---
title: screenshot
level: 4
flag: FLAG{beware_of_parameter_type_confusion!}
writer: ciffelia
badge: true
---

# screenshot

## 問題文

好きなウェブサイトのスクリーンショットを撮影してくれるアプリです。

An application that takes screenshots of your favorite websites.

<https://screenshot-web.wanictf.org>

## 解法

English follows Japanese.

まずはアプリケーションの概要を確認します。

- URLを指定するとそのページのスクリーンショットをPNG画像として返してくれるアプリです。
- URLは `/api/screenshot?url=https%3A%2F%2Fwww.google.com%2F` のようにGETパラメータで指定します。
- バックエンドはJavaScript (Node.js)で実装されており、Headless Chromiumでページを開いて内容をレンダリングしています。
- フラグは`/flag.txt`に格納されています。

ユーザーが指定したURLにサーバーがアクセスするアプリケーションにおいては、SSRF (Server Side Request Forgery)と呼ばれる攻撃手法が知られています。

[SSRF(Server Side Request Forgery)徹底入門 | 徳丸浩の日記](https://blog.tokumaru.org/2018/12/introduction-to-ssrf-server-side-request-forgery.html)

Chromeでは、`file:///etc/passwd`のように`file://`で始まるURLを使ってローカルファイルの内容を表示することができます。この問題ではこれを使い、`file:///flag.txt`のスクリーンショットを撮らせることができないか試してみましょう。試しにフォームに`file:///flag.txt`を入力して送信すると、残念ながらBad Requestと表示されてしまい、攻撃は失敗します。

なぜ`file:///flag.txt`を送信するとエラーが表示されるのか、配布されているソースコードを読んで確認してみます。`index.js`を開くと20行目に次の処理があります。

```js
if (!req.query.url.includes("http") || req.query.url.includes("file")) {
  res.status(400).send("Bad Request");
  return;
}
```

`req.query.url`、つまりクエリ文字列の`url`パラメータの値を検査し、部分文字列として`http`が含まれていなかったり`file`が含まれていたりするとエラーを返す仕組みになっているようです。

```js
console.log(req.query.url) // => "file:///flag.txt"
console.log(req.query.url.includes("http")) // => 文字列に"http"が含まれるか (false)
console.log(req.query.url.includes("file")) // => 文字列に"file"が含まれるか (true)
```

実はこのチェックに穴があります。

`?url=abc&url=def`のように`url`パラメータが複数含まれるクエリが渡されたとき、`req.query.url`の内容は配列になります。配列における`includes()`は特定の要素が含まれるかどうかを返すメソッドなので、特定の文字列が部分文字列として含まれているかをチェックすることができません。

```js
console.log(req.query.url) // => ["abc", "def"]
console.log(req.query.url.includes("http")) // => 配列に"http"という要素が含まれるか (false)
console.log(req.query.url.includes("file")) // => 配列に"file"という要素が含まれるか (false)
```

したがって、`?url=file%3A%2F%2F%2Fflag.txt&url=http`のようなクエリ文字列が渡されたとき、チェックをすり抜けてしまうことがわかります。このようなバグはparameter type confusionと呼ばれることがあります。

`url`パラメータが複数渡されたとき、Chromiumで開くURLはどうなるのか見てみましょう。`index.js`の27行目に次のような処理があります。

```js
const params = new URLSearchParams(req.url.slice(req.url.indexOf("?")));
await page.goto(params.get("url"));
```

URLの`?`より後ろを抜き出し、`URLSearchParams`を使って`url`パラメータの値を取り出しています。`URLSearchParams.prototype.get()`の仕様を読むと、同じパラメータが複数渡された際には最初のものを返すことになっています。つまり、`?url=file%3A%2F%2F%2Fflag.txt&url=http`に対しては`file:///flag.txt`を返すことになります。

- [URL Standard](https://url.spec.whatwg.org/#dom-urlsearchparams-get)
- [URLSearchParams.get() - Web API | MDN](https://developer.mozilla.org/ja/docs/Web/API/URLSearchParams/get)

したがって、`/api/screenshot?url=file%3A%2F%2F%2Fflag.txt&url=http`にアクセスすると、チェックをすり抜けてChromeに`file:///flag.txt`を開かせることができます。

なお、開催中に見つかった非想定解として、`filE:///http/../flag.txt`をURLとして指定するというものがあります。こちらでも同様にフラグを得ることができます（報告ありがとうございます）。

---

First, review the application overview.

- The application returns a screenshot of any page as a PNG image.
- The URL is specified by a GET parameter like `/api/screenshot?url=https%3A%2F%2Fwww.google.com%2F`.
- The backend is implemented in JavaScript (Node.js) and opens the page with Headless Chromium to render the content.
- The flag is stored in `/flag.txt`.

In applications where the server accesses the URL specified by the user, an attack technique called SSRF (Server Side Request Forgery) is known.

(Note: The following article is written in Japanese; you may find a similar information in English by Googling.)

[A Thorough Introduction to SSRF (Server Side Request Forgery) | Hiroshi Tokumaru's Diary](https://blog.tokumaru.org/2018/12/introduction-to-ssrf-server-side-request-forgery.html)

Chrome can display the contents of local files using URLs starting with `file://`, such as `file:///etc/passwd`. Let's try to use this to see if we can get it to take a screenshot of `file:///flag.txt`. If you enter `file:///flag.txt` in the form and submit it, unfortunately, a "Bad Request" error shows up and the attack will fail.

Let's read the distributed source code to see why an error is displayed when we submit `file:///flag.txt`. If you open `index.js`, you will find the following code on line 20.

```js
if (!req.query.url.includes("http") || req.query.url.includes("file")) {
  res.status(400).send("Bad Request");
  return; }
}
```

It seems that the system inspects the value of the `req.query.url`, or `url` parameter of the query string, and returns an error if it does not contain `http` or contains `file` as a substring.

```js
console.log(req.query.url) // => "file:///flag.txt"
console.log(req.query.url.includes("http")) // => if the string coitains "http" (false)
console.log(req.query.url.includes("file")) // => if the string coitains "file" (true)
```

Actually, there is a flaw in this check.

When a query with multiple `url` parameters is passed, such as `?url=abc&url=def`, the contents of `req.query.url` will be an array. Since `Array.prototype.includes()` is a method that returns whether a particular element is included or not, it cannot check whether a particular string is included as a substring.

```js
console.log(req.query.url) // => ["abc", "def"].
console.log(req.query.url.includes("http")) // => if the array contains "http" (false)
console.log(req.query.url.includes("file")) // => if the array contains "file" (false)
```

Thus, when a query string such as `?url=file%3A%2F%2F%2Fflag.txt&url=http` is passed, it will pass the checks. Such a bug is sometimes called parameter type confusion.

Let's look at what happens to the URLs opened in Chromium when multiple `url` parameters are passed. In line 27 of `index.js`, we see the following

```js
const params = new URLSearchParams(req.url.slice(req.url.indexOf("?")));
await page.goto(params.get("url"));
```

This code extracts the back part of the URL after the `?`, and uses `URLSearchParams` to retrieve the value of the `url` parameter. If you read the specification of `URLSearchParams.prototype.get()`, you will see that when multiple identical parameters are passed, the first one is returned. That is, `?url=file%3A%2F%2F%2Fflag.txt&url=http` will return `file:///flag.txt`.

- [URL Standard](https://url.spec.whatwg.org/#dom-urlsearchparams-get)
- [URLSearchParams: get() method - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams/get)

Thus, accessing `/api/screenshot?url=file%3A%2F%2F%2Fflag.txt&url=http` will allow you to pass the checks and have Chrome open `file:///flag.txt`.

Note that an unintended solution found during the event is to specify `filE:///http/../flag.txt` as the URL. You can also get the flag this way (thanks for the report).
