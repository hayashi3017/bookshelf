# Executing Multiple Futures at a Time
複数の非同期関数を並行処理する方法の例

## join!
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
### 基本
複数の非同期処理のうち一つが完了すれば、応じた処理をする。
他の非同期処理の完了は待たない。例えば副作用関数や不純関数の場合はどういう扱いになるのだろうか？
`select!`も式なのでそれぞれの返り値は同じ型でなければならない。

syntax: `<pattern> = <expression> => <code>,`

`select!`に渡すFutureはUnpinと[`futures::future::FusedFuture`](https://docs.rs/futures/latest/futures/future/trait.FusedFuture.html)を実装する必要がある[^note3]
Unpinはselectが可変参照を取得するために必要。moveしては後続処理ができないらしい。
FusedFutureはselectが完了した後にpollしないように必要。FusedFutureは互いに完了したかどうかを追跡する。selectループで完了していないFutureのみpollするために必要。
future::readyによって変えるFutureはFusedFutureを実装しているので、再度pollされないような仕組み。

- [`futures::select`](https://docs.rs/futures/latest/futures/macro.select.html)
  - [Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=cf145e50948de8f1c82a5ddcb16e8c7f)
  - TODO: なぜ結果が一つに収束するのだろうか
- [`tokio::select`](https://docs.rs/tokio/latest/tokio/macro.select.html)

Streamは[`futures::stream::FusedStream`](https://docs.rs/futures/latest/futures/stream/trait.FusedStream.html)に対応している。

### Concurrent tasks in a select loop

[`futures::future::Fuse::terminated`](https://docs.rs/futures/latest/futures/future/struct.Fuse.html#method.terminated)は既に完了したFutureをFuseできるので、selectループで便利らしい。

### source code
- [select in futures - Rust](https://docs.rs/futures/latest/futures/macro.select.html)
  - [select_internal in futures_macro - Rust](https://docs.rs/futures-macro/latest/futures_macro/macro.select_internal.html)
    - [futures-rs/futures-macro/src/select.rs at aafe554b02cbac19d396512b36bce8b688a18115 · rust-lang/futures-rs](https://github.com/rust-lang/futures-rs/blob/aafe554b02cbac19d396512b36bce8b688a18115/futures-macro/src/select.rs#L128-L327)


## Spawning

spawnはJoinHandleを返す。

JoinHandleはFutureを実装しているのでawaitするまで結果を得られない。[^note88]

mainタスクとspawnされたタスクとのやり取りとして、channelsを利用する。

---
[^note1]: [join! - Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/06_multiple_futures/02_join.html)<br />
The value returned by join! is a tuple containing the output of each Future passed in.

[^note2]: [rust - Concurrent async/await with sleep - Stack Overflow](https://stackoverflow.com/questions/70959134/concurrent-async-await-with-sleep)<br />
Since the standard/original thread::sleep is blocking, it turns out that the async library is providing async_std::task::sleep( ... ) which is the nonblocking version for sleep. 

[^note3]: [select in futures - Rust](https://docs.rs/futures/latest/futures/macro.select.html)<br />
Futures directly passed to select! must be Unpin and implement FusedFuture.

[^note88]: [Spawning - Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/06_multiple_futures/04_spawning.html)<br />
The JoinHandle returned by spawn implements the Future trait, so we can .await it to get the result of the task.