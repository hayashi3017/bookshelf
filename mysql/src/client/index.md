# Client


user`foo`に対して権限を付与する。
```mysql
grant all privileges on creation.* to 'foo'@'%';
flush privileges;
```
`@`の後ろはホスト名を指し、`%`はワイルドカードを意味する
[MySQL :: MySQL 8.0 リファレンスマニュアル :: 6.2.4 アカウント名の指定](https://dev.mysql.com/doc/refman/8.0/ja/account-names.html)


