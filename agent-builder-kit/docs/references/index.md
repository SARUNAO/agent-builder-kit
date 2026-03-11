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
- canvas の reference band 正本は `docs/PRODUCT_SENSE.md`, `docs/DESIGN.md`, `docs/HUMAN_MANUAL.md`, `docs/exec-plans/active/attention-queue.md` の direct source とする
- この directory の `roles.md`, `lifecycle.md`, `review-policy.md` は support reference asset であり、reference band の直接入力ではない
- package 側では keep しつつ、語彙 drift があれば refresh 候補、利用実態が消えたら archive 候補として扱う

## 現時点の整理メモ
- `roles.md`
  - keep 寄り
  - ただし `program-board` など旧語彙が残るため refresh 候補
- `lifecycle.md`
  - keep 寄り
  - ただし `chunk-sheet` や `program-board` など旧語彙が残るため refresh 候補
- `review-policy.md`
  - keep 寄り
  - ただし `task-review skill`, `chunk-close skill` など旧 alias が残るため refresh 候補

## summary note の書き方
- `product-sense`, `design`, `human-manual`
  - 短い見取り図だけを書く
  - 本体 docs の全文転載はしない
- `attention-queue`
  - runtime summary として current priority だけを抜き出す
  - planning source そのものは本体 docs に残す
