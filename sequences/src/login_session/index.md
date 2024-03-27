# login_session

簡単にパターン別にまとめてみます。

- Traditional
- Token based
- Traditional + KV
- Token based + Refresh token

保存箇所（Header or cookie）の違いによるセキュリティリスクの違いも考慮する必要があるかもしれない。
OAuth2.0の仕様としてRefresh tokenが存在するようなので、参考になるかもしれない。

## Traditional
Session tokenをクライアントへ持たせる
クライアントはリクエスト毎にSession tokenをサーバーへ渡す
サーバーはSession tokenを検証のため、DBへユーザ情報取得クエリを実行する
Session tokenの検証が通ればリクエストを処理し、クライアントへ成功レスポンスを返す

```mermaid

```
![traditional session image](images/session_traditional.png)

- cons
  - 時間がかかるDBへのクエリ実行が毎回行われている点

対策として、下記がある
- サーバー上へ保存する
- ロードバランサーでsticky sessionにする
- Token based

## Token based
認証用トークンとして主要なJWTを例にします。
ポイントはJWT自身に認証情報を持たせるので、バックエンドがステートレスになる点

JWT tokenをクライアントへ持たせる
クライアントはリクエスト毎にJWT tokenをサーバーへ渡す
サーバーは自身でJWTを検証し、ユーザ情報をJWTから取得する
JWT tokenの検証が通ればリクエストを処理し、クライアントへ成功レスポンスを返す

![token based session image](images/session_token.png)

- cons
  - JWTの失効を制御できない点

JWTの失効をサーバーで管理すればいいと考えるかもしれませんが、それではTraditionalと同じ問題が発生します。つまりDBへのクエリ実行が行われることになります。[^note44]

JWTでは有効期限の制御を捨てて、短命なトークンを前提とした利用が主要となっている。
トークンが短命でも問題のない、サーバー間認証に適している。

## Traditional + KV
遅いDBへのクエリはKVやキャッシュサーバーを利用しようという案
これが主流かもしれない、根拠なし

![traditional + kv session image](images/session_traditional-kv.png)



## Token based + Refresh token

Refresh tokenはaccess tokenの有効期限が切れた際に再発行を求めるためのもので、これによりユーザーは再ログインをする必要がない[^note59]

Refresh token自体にもaccess tokenを発行することができるので同じぐらいの認証情報を持つと考えるが、ユーザ情報を含まないので漏洩してもaccess tokenを発行されなければいい。
access tokenの発行にはRefresh tokenの検証を行うことで悪用を防ぐことができるのかもしれない。

Auth0では再利用の自動検知を行っている[^note63]。
まず前提として、Refresh token Rotationを行っており、Refresh tokenを利用すると新しいRefresh tokenも返すらしい。

再利用の自動検知によって攻撃者がRefresh tokenを盗みaccess token生成に利用した際に、既にRefresh tokenが使用されていればtoken familyに含まれるすべてのRefresh tokenを無効化するような挙動をとるらしい。
再利用するのは正規ユーザーとその他（攻撃者）が競合したケースのみ。
再利用を検知すると全てのRefresh tokenを無効化するので、攻撃者が先にRefresh tokenを使用した場合もRefresh tokenによるリスクは抑えられる。ただこの場合はaccess tokenが生存する間は攻撃が可能になってしまうか。（といってもTraditionalでもsession tokenが漏洩したら同じか。仕様レベルで有効期間がついている分JWTの方がよい）

結局token familyを管理するならば、パフォーマンス的にはTraditionalと同じではないかと思う。
利点は・・JWTにすることでサーバーは認証情報ステートレスになる、サーバーから認証機能を分離して考えられる、ぐらいか。


```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```


---
[^note44]: [JSON Web Tokens (JWT) are Dangerous for User Sessions—Here’s a Solution | Redis](https://redis.com/blog/json-web-tokens-jwt-are-dangerous-for-user-sessions/)<br />
One popular solution is to store a list of “revoked tokens” in a database and check it for every call. And if the token is part of that revoked list, then block the user from taking the next action. But then now you are making that extra call to the DB to check if the token is revoked and so deceives the purpose of JWT altogether. 

[^note59]: [What Are Refresh Tokens and How to Use Them Securely](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)<br />
That is, a refresh token is a credential artifact that lets a client application get new access tokens without having to ask the user to log in again.

[^note63]: [What Are Refresh Tokens and How to Use Them Securely](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)<br />
Our identity platform offers refresh token rotation, which also comes with automatic reuse detection.
