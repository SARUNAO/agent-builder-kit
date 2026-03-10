# References

generic 配布 package には builder 固有の project-specific reference 本文を同梱しない。

- bootstrap 後の runtime reference は `docs/references/` 配下へ生成する
- builder 自身の source 棚卸しは配布 package の外で管理する
- source asset として `roles.md`, `lifecycle.md`, `review-policy.md` を同梱する

## 同梱 source asset
- [roles.md](./roles.md)
- [lifecycle.md](./lifecycle.md)
- [review-policy.md](./review-policy.md)

## 正本契約
- canvas の reference band が直接読む正本は `docs/references/*.md`
- ただし `product-sense`, `design`, `human-manual` は summary view であり、意味上の本体は `docs/*.md` 側にある
- `attention-queue` の意味上の本体は `docs/exec-plans/active/attention-queue.md`
- 各 reference note は `source_doc` を持ち、本体 docs への導線を明示する

## summary note の書き方
- `product-sense`, `design`, `human-manual`
  - 短い見取り図だけを書く
  - 本体 docs の全文転載はしない
- `attention-queue`
  - runtime summary として current priority だけを抜き出す
  - planning source そのものは本体 docs に残す
