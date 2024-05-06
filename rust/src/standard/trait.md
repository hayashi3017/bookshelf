# trait


- 拡張トレイト
  - 既存の方にメソッドを追加するためだけのトレイト
- 



## 型関連関数

トレイトに型関連関数を持たせることができる。
トレイトオブジェクトでは型関連関数をサポートしていない。
`where Self: Sized`を指定することでトレイトオブジェクトでの使用を除外する、これでトレイトオブジェクトを作ることができるようになる。つまり、型関連関数は使用できないが関連関数は使用できる状態になる。


## 関連型

トレイトでメソッドを実行する以上のことをしたいなら、関連型は有用。
```rust
pub trait Iterator {
  type Item;
  fn next(&mut self) -> Option<Self::Item>;
}
```

`Mul<i32>`と`Mul<f64>`は異なるトレイトとして認識される。
ジェネリックトレイトは孤児ルールに関して特別な待遇を受けている。
例えば`WindowSize`を自クレートで定義したなら、`impl Mul<WindowSize> for i32`のように外部トレイトを外部の型へ実装できる。トレイトが独自であり衝突することがないからだ。
`impl<T> Mul<WindowSize> for Vec<T>`のようにジェネリックにすることもできる。
```rust
pub tarit Mul<RHS> {
  type Output;
  fn mul(self, rhs: RHS) -> Self::Output;
}
```


## impl Trait

```rust
fn cyclical_zip(v: Vec<u8>, u: Vec<u8>) -> impl Iterator<Item=u8> {
  v.into_iter().chain(u.into_iter()).cycle()
}
```
利点
- より関数の意図を表す場合がある
- インターフェースだけを指定できるので変更に強い

注意点
- impl Traitは静的ディスパッチの一つなので、コンパイル時にその関数が返す型が決定していなければならない
- トレイトメソッドではimpl Traitを返り値の型として指定できない。自由関数や特定の型に関連した関数に対してのみ使用できる
- `print::<i32>(42)`のように型を明示して呼び出すことはできない。ジェネリクス関数ではできる
- impl Traitでは特定の無名型パラメータが割り当てられる？　したがって実現できるのは単純なジェネリクスのみ。引数の型に関係性を持つような関数は表現できないらしい。

下記は同等だが、impl Taritでは呼び出し方に制限がある。
```rust
// ジェネリクス関数
fn print<T: Display>(val: T) {
  println!("{}", val);
}
print::<i32>(42);

// impl Trait
fn print(val: impl Display) {
  println!("{}", val);
}
print(42);
```

## 関連定数
構造体や列挙型と同じように、トレイトにも関連定数を持たせることができる。
トレイトの場合は値を指定する必要はない(指定してもよい)。値は実装の際に指定できる。

```rust
trait Greet {
  const GREETING: &'static str = "Hello";
  const TYPE: Self;
}
```

注意点
- トレイトオブジェクトでは使用できない。コンパイル時に実装に関する型情報を用いて正しい値を選択するから


## トレイトオブジェクト
traitを利用して多層性を表現する方法の一つ

コンパイル時にサイズが決まっていなければならないものーー変数などでは`dyn Write`型を指定できない。
したがって例えば参照ならばサイズが決まるので指定できる。
このような、トレイト型への参照をトレイトオブジェクトと呼ぶ。

```rust
let mut buf: Vec<u8> = vec![];
// error
let writer: dyn Write = buf;
// ok
let writer: &mut dyn Write = &mut bef;
```

メモリ上ではファットポインタ
- 値へのポインタ
- 値の型を表すテーブル(仮想テーブル)へのポインタ

Rustの仮想テーブルはコンパイル時に一度だけ作られ、同じ型のすべてのオブジェクトによって共有される。

Rustは通常の参照を必要に応じて自動的にトレイトオブジェクトへ変換する
say_helloの引数の型は&mut dyn WriteだがFileはWriteトレイトを実装しているのでlocal_fileはそのまま渡してもトレイトオブジェクトヘ自動変換される。
```rust
let mut local_file: File = File::create("hello.txt");
say_hello(&mut local_file)?;
```

