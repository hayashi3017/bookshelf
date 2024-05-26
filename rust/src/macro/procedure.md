# procedure

## Attribute macros

[`items`]へ[`outer attributes`] を定義するマクロ。つまり[`Trait`]実装などを継承させるマクロ。

`proc_macro_attribute`[`Attribute`]を使ってpublicな[`function`]へ定義する。

### example
sqlxより、
```rust
#[cfg(feature = "macros")]
#[proc_macro_attribute]
pub fn test(args: TokenStream, input: TokenStream) -> TokenStream {
    let input = syn::parse_macro_input!(input as syn::ItemFn);

    match test_attr::expand(args.into(), input) {
        Ok(ts) => ts.into(),
        Err(e) => {
            if let Some(parse_err) = e.downcast_ref::<syn::Error>() {
                parse_err.to_compile_error().into()
            } else {
                let msg = e.to_string();
                quote!(::std::compile_error!(#msg)).into()
            }
        }
    }
}
```
inputは[`syn::parse`]でパースする。[`syn::parse::Parse`]traitを実装済みであれば上記のようにasでパース先を指定できる。(asはキャストなどではなくマクロ定義の一部であることに注意)



[`function`]: https://doc.rust-lang.org/reference/items/functions.html
[`Attribute`]: https://doc.rust-lang.org/reference/attributes.html
[`Trait`]: https://doc.rust-lang.org/reference/items/traits.html
[`items`]: https://doc.rust-lang.org/reference/items.html
[`outer attributes`]: https://doc.rust-lang.org/reference/attributes.html

[`syn::parse`]: https://docs.rs/syn/latest/syn/parse/index.html
[`syn::parse::Parse`]: https://docs.rs/syn/latest/syn/parse/trait.Parse.html