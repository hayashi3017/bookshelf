# test
[テストの記述法 - The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/ch11-01-writing-tests.html)

Rustには簡単なテストフレームワークが組み込まれている。
テストはマルチスレッドで並列実行される。これは`carto test -- --test-threads 1`のように調整できる。
テストが失敗した結果のみ出力されるので、成功結果も出力したければ`cargo test -- --no-capture`とする。

## Unit test
[ユニットテスト - Rust By Example 日本語版](https://doc.rust-jp.rs/rust-by-example-ja/testing/unit_testing.html)

### assersionする

テストは[#[test]属性](https://doc.rust-lang.org/std/prelude/v1/attr.test.html)が付与された通常の関数である。
下記を利用する。

- [std::assert](https://doc.rust-lang.org/std/macro.assert.html)
- [std::assert_eq](https://doc.rust-lang.org/std/macro.assert_eq.html)

上記は非テストでも利用できる。つまりリリースビルドにも入ってしまう。
デバッグビルド時のみ有効にしたければ下記を利用する。

- [std::debug_assert](https://doc.rust-lang.org/std/macro.debug_assert.html)
- [std::debug_assert_eq](https://doc.rust-lang.org/std/macro.debug_assert_eq.html)

もっといえば、テスト時のみ実行するように#[cfg]属性で設定するのが慣習となっている。

### panicする

エラーが起こる場合を正常としたテストをしたいなら、#[should_panic]属性を利用する。
パニックが起こることが自明な静的コードの場合、#[allow]属性でコンパイラへ指示する。


## Integration test
[インテグレーションテスト - Rust By Example 日本語版](https://doc.rust-jp.rs/rust-by-example-ja/testing/integration_testing.html)

Cargoは`src/`と同じ階層の`tests/`配下を統合テストとして扱う。
クレートを外部のユーザの世界から見る。つまりクレートの公開APIをテストすることがポイント。

`cargo test`: 単体テスト、統合テストを実行する
`cargo test --test foo`: `tests/foo.rs`に書かれた統合テストを実行する


