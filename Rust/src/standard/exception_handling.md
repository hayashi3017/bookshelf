# Exception Handling

## 📚 Reference

- https://doc.rust-lang.org/std/result/index.html
- https://doc.rust-lang.org/std/option/index.html

## 📝 Report



## はじめに

RustのResult, Optionについて整理しておきたい。
どちらも列挙型です。これらの型を用いることで、例外処理を扱います。
Rustのバージョンは1.75.0です。

## Result型

```rust
enum Result<T, E> {
   Ok(T),
   Err(E),
}
```

### Methods

(ほぼOptionと同じだ)


## Option型

```rust
pub enum Option<T> {
    None,
    Some(T),
}
```

`Option<T>`型は`None`または`Some(T)`を指します。
`None`は他言語でいうnullです、値がないことを示します。
`Some(T)`はT型の値を持つSome型を示します。

### Methods
使い分けが難しいと感じるものを整理します。

#### Some(T)を取り出す
`None`が返る場合の挙動が下記のように異なります。

- [exprect](https://doc.rust-lang.org/std/option/enum.Option.html#method.expect)
  - 指定した文言でpanicさせる
- [unwrap](https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap)
  - コンパイラ？生成文言でpanicさせる
- [unwrap_or](https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or)
  - 指定した値を返す
- [unwrap_or_default](https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or_default)
  - [std::default::Default](https://doc.rust-lang.org/std/default/trait.Default.html)を返す
- [unwrap_or_else](https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or_else)
  - 指定した[std::ops::FnOnce](https://doc.rust-lang.org/std/ops/trait.FnOnce.html)の戻り値を返す

#### 型を変換する

##### Result型へ

- [ok_or](https://doc.rust-lang.org/std/option/enum.Option.html#method.ok_or)
  - `Some(T)`を`Ok(T)`へ、`None`を`Err(err)`へ。errは指定した値。
- [ok_or_else](https://doc.rust-lang.org/std/option/enum.Option.html#method.ok_or_else)
  - `Some(T)`を`Ok(T)`へ、`None`を`Err(err)`へ。errは指定した[std::ops::FnOnce](https://doc.rust-lang.org/std/ops/trait.FnOnce.html)。
- [transpose](https://doc.rust-lang.org/std/option/enum.Option.html#method.transpose)
  - `Option<Result<T>>`を`Result<Option<T>>`へ

##### Someを変える

- [filter](https://doc.rust-lang.org/std/option/enum.Option.html#method.filter)
  - `true`を返す値を`Some(T)`とする
- [flatten](https://doc.rust-lang.org/std/option/enum.Option.html#method.flatten)
  - `Option<Option<T>>`を`Option<T>`へ
- [map](https://doc.rust-lang.org/std/option/enum.Option.html#method.map)
  - `Option<T>`を`Option<U>`へ

##### 型を変える

`Some(T)`の場合、指定した[std::ops::FnOnce](https://doc.rust-lang.org/std/ops/trait.FnOnce.html)の戻り値を返す

- [map_or](https://doc.rust-lang.org/std/option/enum.Option.html#method.map_or)
  - `None`の場合、指定した値を返す
- [map_or_else](https://doc.rust-lang.org/std/option/enum.Option.html#method.map_or_else)
  - `None`の場合、指定した[std::ops::FnOnce](https://doc.rust-lang.org/std/ops/trait.FnOnce.html)の戻り値を返す


### その他
下記は省略しました、公式ドキュメントを参照しましょう。

- Querying the variant
- Adapters for working with references 参照型との調整
- Boolean operators
- Comparison operators
- Iterating over Option
- Collecting into Option
- Modifying an Option in-place

## 共通

### `?` operator

`?`オペレーターを使用した値は
`None`が返る場合は近しいブロックを`None`で抜けます。
それ以外は`Some(T)`を`unwrap()`した値になります。


