# Send

非同期関数のFutureがSendかどうかは、Sendでない方が.awaitをまたがって生存しているかどうかで決まる。[^note3]


---
[^note3]: [Send Approximation - Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/07_workarounds/03_send_approximation.html)<br/>
Whether or not an async fn Future is Send is determined by whether a non-Send type is held across an .await point. 