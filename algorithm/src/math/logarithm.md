# Logarithm

Rustプログラムで常用対数表の一部を出力する

```rust
fn main() {
    println!("Number\tLog10");
    for i in 1..=10 {
        let log_value = (i as f64).log10();
        println!("{}\t{}", i, log_value);
    }
}
```

## 対数を用いた近似

Q. \\( 2^{10} \\)の近似値を求めよ。

\\( \log_{10}2^{10} = 10 \cdot \log_{10}2 \\)

\\( \log_{10}2 \simeq 0.310 \\) より

\\( 10 \cdot \log_{10}2 \simeq 10 \cdot 0.310 = 3.10 = 3 + 0.1  \\)

それぞれを常用対数で表現すると

\\( 3 + 0.1 \simeq \log_{10}10^3 + \log_{10}1.26 = \log_{10}(1.26 \times 10^3 ) \\)

つまり、\\( \log_{10}2^{10} \simeq \log_{10}(1.26 \times 10^3 ) \\)

\\( 2^{10} = 1024\\)であるから、計算量を予測する用途などでは十分近似できているといえる。
