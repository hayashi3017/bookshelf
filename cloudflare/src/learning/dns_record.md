# DNS record
[DNSレコードとは？ | Cloudflare](https://www.cloudflare.com/ja-jp/learning/dns/dns-records/)

- DNSレコード（ゾーンファイル）
  - 権威DNSサーバー内に存在する
  - ドメインに関する情報の提供を指示する
    - そのドメイン名に関連付けられたIPアドレスや、ドメインに対するリクエストを処理する方法など
  - 一連のテキストファイルから構成される
    - DNSシンタックスとして知られる方法で書かれる
  - TTL (time-to-live; 存続時間)がある

- A record
- AAAA record
- CNAME record
- MX record
- TXT record
- NS record
- SOA record
- SOA record
- SRV record
- PTR record


## A record
Address record.
与えられたドメインのIPアドレスを示す
IPv4
デフォルトTTLは14,400s(240min)
ほとんどのWebサイトはA recordが1つだが複数持つこともできる


## CNAME record
Canonical NAME
正規のドメイン名を意味する
Aレコードの代わりに使用される
IPアドレスではなくドメイン名を示す


