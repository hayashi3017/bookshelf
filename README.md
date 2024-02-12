This is my book-shelf including books about software development.

- Hosts by CoudFlare Pages
- CI/CD by Github Actions
- Build by mdbook

## How to use

### Create New Book

```bash
mdbook init foo --title foo --ignore git
# cp book.toml foo/book.toml
```


### Book Preview

```bash
mdbook serve --open
```

### Book Deploy
Add below to `.github/workflows/deploy.yml`, and push main branch.
Then deployment is complete by GitHub Actions.
FIXME: Automation this.

```yml
      - name: Check Cache foo
        id: cache_check_foo
        uses: actions/cache@v4
        with:
          path: ./book
          key: ${{ runner.os }}-${{hashfiles('./foo/src/**.md')}}
      - name: Generate Book foo
        if : steps.cache_check_foo.outputs.cache-hit != 'true'
        run: |
          ./generate-book.py foo
      - name: Save Cache foo
        if : steps.cache_check_foo.outputs.cache-hit != 'true'
        uses: actions/cache/save@v4
        with:
          path: ./book/foo
          key: ${{ runner.os }}-${{hashfiles('./foo/src/**.md')}}
```

## How to develop

### about document tool
mdbookを使用していますが、[mkdocs](https://www.mkdocs.org/)へ変更し同じようにCloudFlare Pagesへデプロイできると思われます。

### about directory tree

ローカルで内容確認できるように、フォルダ構成はネストを避けて並列にしています。
フォルダ構成をネストして管理したくなった場合は、[このコミット](00ff17cc7cc16d9a824d69d16643b49b1bad88b4)を参照してください。WIP
（ネストした場合はローカルで確認しづらくなりますが、慣れて確認する必要が無くなるとネストしたくなるかもしれない。）

```md
<!-- ネスト -->
- /text
  - subjects
    - foo
    - bar
    - baz

<!-- 並列 -->
- subjects
- foo
- bar
- baz
```

### limits

> 20,000 (max files) * 25 MiB (max file size)
> https://community.cloudflare.com/t/cloudflare-pages-total-build-size-limit/512140/5

> Cloudflare Pages sites can contain up to 20,000 files.
> ...
> The maximum file size for a single Cloudflare Pages site asset is 25 MiB.
> https://developers.cloudflare.com/pages/platform/limits/

初期状態bookのビルド成果物で43ファイル。つまり100bookほどまで問題なさそう。
ファイルサイズも問題なさそう。

今後、mdbookが複数管理に対応すれば多少軽減される可能性があるので、確認しておきたい。
https://github.com/rust-lang/mdBook/issues?q=multiple+book.toml
https://github.com/rust-lang/mdBook/issues/1666
