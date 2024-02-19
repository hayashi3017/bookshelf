# restrictions
[HTML Standard](https://html.spec.whatwg.org/multipage/introduction.html#restrictions-on-content-models-and-on-attribute-values)

- 表現されたセマンティクスに矛盾がある場合
- デフォルトのスタイルが混乱を招きやすい場合
- etc...


## 表現されたセマンティクスに矛盾がある場合

例）矛盾
```html
<!-- セパレーターが同時にセルになることはない -->
<hr role="cell">
<!-- ラジオボタンがプログレスバーになることはない -->
<input type=radio role=progressbar>
```

## デフォルトのスタイルが混乱を招きやすい場合

例）インラインボックスがブロックボックスを含む
```html
<span>
  foo
  <div>bar</div>
</span>
```

例）対話型コンテントのネスト

```html
<button>
  foo
  <textarea></textarea>
</button>
```

メモ：aタグの子要素には対話型コンテンツを含めることができない
> The a element can be wrapped around entire paragraphs, lists, tables, and so forth, even entire sections, so long as there is no interactive content within (e.g., buttons or other links).
> https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-a-element




