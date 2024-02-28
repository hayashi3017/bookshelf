# Executing Multiple Futures at a Time
複数の非同期関数を並行処理する方法の例

## join!
シングルスレッドでも可能。
`join!`が返す値は、各Future結果のタプル。[^note1]
Futureが`Result`を返す場合、`try_join!`がよいらしい。

### example
検証時のsleepとして、[`std::thread::sleep`](https://doc.rust-lang.org/std/thread/fn.sleep.html)は同期的にブロックしてしまうため、非同期用のsleepが必要。[^note2]

[`tokio::time::sleep`](https://docs.rs/tokio/latest/tokio/time/fn.sleep.html)を使用した例

[Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=ba8eeae7806dab4fa76f5da6dfac5746)

```rust,edition2021
use std::time::Duration;

async fn dance1() { 
    println!("dance1.");
    tokio::time::sleep(Duration::from_secs(10)).await;
    println!("dance1.");
}
async fn dance2() { 
    println!("dance2.");
    tokio::time::sleep(Duration::from_secs(1)).await;
}
async fn dance3() { 
    println!("dance3.");
    tokio::time::sleep(Duration::from_secs(1)).await;
}

#[tokio::main]
async fn main() {
    tokio::join!(dance1(), dance2(), dance3());
}
```

- `std::thread::sleep`を使用した失敗例
  - `futures::join`
    - [Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=7519fd005a6f3908e2c8d1f994f7197d)
  - `tokio::join`
    - [Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=7a7c794aab463bed6ecf032284fe0564)

### 色々なjoin
色々なjoinがある。差分は不明。対応するランタイムが違うだけならよいが。
- [futures::join](https://docs.rs/futures/latest/futures/macro.join.html)
- [tokio::join](https://docs.rs/tokio/latest/tokio/macro.join.html)

### source code
- [join in futures - Rust](https://docs.rs/futures/latest/futures/macro.join.html)
  - [join_internal in futures_macro - Rust](https://docs.rs/futures-macro/latest/futures_macro/macro.join_internal.html)
    - [futures-rs/futures-macro/src/join.rs at aafe554b02cbac19d396512b36bce8b688a18115 · rust-lang/futures-rs](https://github.com/rust-lang/futures-rs/blob/aafe554b02cbac19d396512b36bce8b688a18115/futures-macro/src/join.rs#L50-L86)

## select!
シングルスレッドでも可能。
複数の非同期処理のうち一つが完了すれば、応じた処理をする。
他の非同期処理の完了は待たない。例えば副作用関数や不純関数の場合はどういう扱いになるのだろうか？

WIP

## Spawning



---
[^note1]: [join! - Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/06_multiple_futures/02_join.html)<br />
The value returned by join! is a tuple containing the output of each Future passed in.

[^note2]: [rust - Concurrent async/await with sleep - Stack Overflow](https://stackoverflow.com/questions/70959134/concurrent-async-await-with-sleep)<br />
Since the standard/original thread::sleep is blocking, it turns out that the async library is providing async_std::task::sleep( ... ) which is the nonblocking version for sleep. 

