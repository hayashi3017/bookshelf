# example
[O'Reilly Japan - プログラミングRust 第2版](https://www.oreilly.co.jp/books/9784873119786/)からチュートリアル。

マクロ定義/展開はコンパイル初期のコード読み込み時点で行われる。
マクロ呼び出しは定義後でなければならない。

マクロパターンはコードに対する正規表現のようなもので、トークンという単位に対して操作を行う。コメントやスペースはトークンではないのでいくら入れてもマッチに影響しない。
出力テンプレートでは繰り返しパターンを利用できる。

TODO:
`<[_]>`などの表現について

---


### [sqlx::query_as](https://docs.rs/sqlx/latest/sqlx/macro.query_as.html)
WIP: テスト的に下記へ記しておく。到底すべてまとめられるわけではないので、今後のまとめ方次第では削除する。

```rust
#[macro_export]
#[cfg_attr(docsrs, doc(cfg(feature = "macros")))]
macro_rules! query_as (
    ($out_struct:path, $query:expr) => ( {
        $crate::sqlx_macros::expand_query!(record = $out_struct, source = $query)
    });
    ($out_struct:path, $query:expr, $($args:tt)*) => ( {
        $crate::sqlx_macros::expand_query!(record = $out_struct, source = $query, args = [$($args)*])
    })
);
```

[sqlx_macros::expand_query](https://docs.rs/sqlx-macros/0.7.4/sqlx_macros/macro.expand_query.html)
```rust
#[proc_macro]
pub fn expand_query(input: TokenStream) -> TokenStream {
    let input = syn::parse_macro_input!(input as query::QueryMacroInput);

    match query::expand_input(input, FOSS_DRIVERS) {
        Ok(ts) => ts.into(),
        Err(e) => {
            if let Some(parse_err) = e.downcast_ref::<syn::Error>() {
                parse_err.to_compile_error().into()
            } else {
                let msg = e.to_string();
                quote!(::std::compile_error!(#msg)).into()
            }
        }
    }
}
```


[proc_macro](https://doc.rust-lang.org/proc_macro/)
[[Rust] Procedural Macroの仕組みと実装方法](https://zenn.dev/tak_iwamoto/articles/890771ea5b8ad3)
[Rust の procedural macro を操って黒魔術師になろう〜proc-macro-workshop の紹介](https://zenn.dev/magurotuna/articles/bab4db5999ebfa)

[syn::parse_macro_input](https://docs.rs/syn/latest/syn/macro.parse_macro_input.html)

[sqlx_macros_core::query::expand_input](https://hirofa.github.io/GreenCopperRuntime/sqlx_macros_core/query/fn.expand_input.html)
```rust
pub fn expand_input<'a>(
    input: QueryMacroInput,
    drivers: impl IntoIterator<Item = &'a QueryDriver>,
) -> crate::Result<TokenStream> {
    let data_source = match &*METADATA {
        Metadata {
            offline: false,
            database_url: Some(db_url),
            ..
        } => QueryDataSource::live(db_url)?,

        Metadata { offline, .. } => {
            // Try load the cached query metadata file.
            let filename = format!("query-{}.json", hash_string(&input.sql));

            // Check SQLX_OFFLINE_DIR, then local .sqlx, then workspace .sqlx.
            let dirs = [
                || env("SQLX_OFFLINE_DIR").ok().map(PathBuf::from),
                || Some(METADATA.manifest_dir.join(".sqlx")),
                || Some(METADATA.workspace_root().join(".sqlx")),
            ];
            let Some(data_file_path) = dirs
                .iter()
                .filter_map(|path| path())
                .map(|path| path.join(&filename))
                .find(|path| path.exists())
            else {
                return Err(
                    if *offline {
                        "`SQLX_OFFLINE=true` but there is no cached data for this query, run `cargo sqlx prepare` to update the query cache or unset `SQLX_OFFLINE`"
                    } else {
                        "set `DATABASE_URL` to use query macros online, or run `cargo sqlx prepare` to update the query cache"
                    }.into()
                );
            };

            QueryDataSource::Cached(DynQueryData::from_data_file(&data_file_path, &input.sql)?)
        }
    };

    for driver in drivers {
        if data_source.matches_driver(&driver) {
            return (driver.expand)(input, data_source);
        }
    }

    match data_source {
        QueryDataSource::Live {
            database_url_parsed,
            ..
        } => Err(format!(
            "no database driver found matching URL scheme {:?}; the corresponding Cargo feature may need to be enabled", 
            database_url_parsed.scheme()
        ).into()),
        QueryDataSource::Cached(data) => {
            Err(format!(
                "found cached data for database {:?} but no matching driver; the corresponding Cargo feature may need to be enabled",
                data.db_name
            ).into())
        }
    }
}
```

