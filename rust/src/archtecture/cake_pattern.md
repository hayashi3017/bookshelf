# cake pattern

## 導入
まずは概念からまとめておきたい。

[Scalaにおける最適なDependency Injectionの方法を考察する 〜なぜドワンゴアカウントシステムの生産性は高いのか〜 #Scala - Qiita](https://qiita.com/pab_tech/items/1c0bdbc8a61949891f1f#cake%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3%E3%82%92%E4%BD%BF%E3%81%86%E6%96%B9%E6%B3%95)

下記はCake PatternによるDIを実装しないパターン。
`UserService`が`UserRepository`のみでなく`UserRepositoryImpl`へ依存しているため、`UserRepositoryImpl`の変更がUserServiceへ影響してしまう。

```scala
trait UserRepository {
  // 略
}

object UserRepositoryImpl extends UserRepository {
  // 略
}

object UserService {
  val userRepository: UserRepository = UserRepositoryImpl // ← ここでImplを参照しているのが問題
  // 略
}
```

下記はCake PatterによるDIを実装したパターン。
独自解釈すると、、
`UserService`: サービス
`UserRepository`: 外部実装の抽象
`UserRepositoryImpl`: 外部実装
があったのに対し、下記を追加実装し、結合箇所は抽象層のみとした。
`UserService`(trait): サービスの抽象
`UserRepositoryComponent`: 「外部実装の抽象」の抽象
`UserRepositoryComponentImpl`: 「外部実装の抽象化」の抽象

```scala
trait UserRepositoryComponent {
  val userRepository: UserRepository

  trait UserRepository {
    // 略
  }
}

trait UserRepositoryComponentImpl extends UserRepositoryComponent {
  val userRepository = UserRepositoryImpl

  object UserRepositoryImpl extends UserRepository {
    // 略
  }
}

trait UserService {
  this: UserRepositoryComponent =>
  // 略
}

object UserService extends UserService with UserRepositoryComponentImpl
```


他
[Minimal Cake Pattern 再考 #テスト - Qiita](https://qiita.com/tayama0324/items/03ba48d3277079f20500)


## Rustでの実践

[RustのDI | κeenのHappy Hacκing Blog](https://keens.github.io/blog/2017/12/01/rustnodi/)
[Cake PatternでDIしてみた | blog.ojisan.io](https://blog.ojisan.io/cake-pattern/)
[Rust で DI | blog.ojisan.io](https://blog.ojisan.io/rust-di/)
