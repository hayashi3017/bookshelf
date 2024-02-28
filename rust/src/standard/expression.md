# expression

Rustはいわゆる式言語の一つ。すべてを式で扱う。[^note]

||C|Rust|
|-|-|-|
|if/switchの扱い|文|式|
|if/switchを式の中で使えるか|No|Yes|


```rust
let status =
  if cpu.temperature <= MAX_TEMP {
    HttpStatus::Ok
  } else {
    HttpStatus::ServerError
  };
```
Rustはif式を変数へ直接bindできるので、三項演算子をもたない。



[^note]: [O'Reilly Japan - プログラミングRust 第2版](https://www.oreilly.co.jp/books/9784873119786/)
