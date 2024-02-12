This is my book-shelf including books about software development.

- Hosts by CoudFlare Pages
- CI/CD by Github Actions
- Build by mdbook

## How to deploy

### bookの新規作成

```bash
mdbook init foo --title foo --ignore git
# cp book.toml foo/book.toml
```


### 動作確認

```bash
mdbook serve --open
```

ローカルで動作確認できるように、フォルダ構成はネストを避けて並列にしています。
フォルダ構成をネストして管理したくなった場合は、[このコミット](00ff17cc7cc16d9a824d69d16643b49b1bad88b4)を参照してください。
（ネストした場合はローカルで確認しづらくなりますが、慣れて確認する必要が無くなるとネストしたくなるかもしれない。）
