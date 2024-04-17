# minimal Cake Pattern

## 導入

[Scalaにおける最適なDependency Injectionの方法を考察する 〜なぜドワンゴアカウントシステムの生産性は高いのか〜 #Scala - Qiita](https://qiita.com/pab_tech/items/1c0bdbc8a61949891f1f#%E6%9C%80%E5%B0%8F%E3%81%AEcake%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3minimal-cake-pattern)


```scala
// インターフェース
trait UsesUserRepository {
  val userRepository: UserRepository
}
trait UserRepository {
  // 略
}

// 実装側
trait MixInUserRepository extends UsesUserRepository {
  val userRepository = UserRepositoryImpl
}
object UserRepositoryImpl extends UserRepository {
  // 略
}

// 利用側
trait UserService extends UsesUserRepository {
  // 略
}
object UserService extends UserService with MixInUserRepository

```



[Minimal Cake Pattern のお作法 #Scala - Qiita](https://qiita.com/tayama0324/items/7f87ee3672b15dd68016)


## Rustでの実践


[Rust の DI を考える –– Part 2: Rust における DI の手法の整理 - paild tech blog](https://techblog.paild.co.jp/entry/2023/06/12/170637)




