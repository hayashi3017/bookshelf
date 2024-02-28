# Pinning

[`core::pin`](https://doc.rust-lang.org/beta/core/pin/index.html)は[`core::marker::Unpin`](https://doc.rust-lang.org/beta/core/marker/trait.Unpin.html)と連動する。

Pinningは`!Unpin`を実装した式がmoveしていないことを示し、asyncブロック内で値への参照を保証する。


## Why

PinningはRustで安全性が十分に担保できていないケースに必要。[^note1]

例）自己参照型
例）侵入的データ構造

### 自己参照型の構造体がmoveすると、自己参照先が不正となる例

[Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=faea832fa05d21403c2ec8e1de6e4398)
```rust
#[derive(Debug)]
struct Test {
    a: String,
    b: *const String,
}

impl Test {
    fn new(txt: &str) -> Self {
        Test {
            a: String::from(txt),
            b: std::ptr::null(),
        }
    }

    fn init(&mut self) {
        let self_ref: *const String = &self.a;
        self.b = self_ref;
    }

    fn a(&self) -> &str {
        &self.a
    }

    fn b(&self) -> &String {
        assert!(!self.b.is_null(), "Test::b called without Test::init being called first");
        unsafe { &*(self.b) }
    }
}

fn main() {
    let mut test1 = Test::new("test1");
    test1.init();
    let mut test2 = Test::new("test2");
    test2.init();

    println!("a: {}, b: {}", test1.a(), test1.b());
    assert_eq!("test1", test1.a());
    assert_eq!("test1", test1.b());
    std::mem::swap(&mut test1, &mut test2);
    println!("a: {}, b: {}", test2.a(), test2.b());
    assert_eq!("test1", test2.a());
    assert_eq!("test1", test2.b());
}
```

Fig 1: Before and after swap
![before and after swap](/images/before_and_after_swap.png)

### 侵入的データ構造の例

WIP: [core::pin - Rust](https://doc.rust-lang.org/beta/core/pin/index.html#an-intrusive-doubly-linked-list)

---
[^note1]: [core::pin - Rust](https://doc.rust-lang.org/beta/core/pin/index.html)<br/>
This concept of “pinning” is necessary to implement safe interfaces on top of things like self-referential types and intrusive data structures which cannot currently be modeled in fully safe Rust using only borrow-checked references.

