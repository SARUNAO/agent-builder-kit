# Gotcha Log

この docs は、初学者や次の worker が詰まりやすい点と、その回避策を残す一次記録の置き場。

## 書き方
- 失敗したこと自体より、何に引っかかったかを短く書く
- 回避策があるなら同じ項目に並べる
- 環境依存なら、その条件も書く

## Entries
- 2026-03-10 / TICKET-2026-03-10-001: `mdbook` 未導入の段階でも block 全体を止めず、まず確認コマンドと導線整備から進められる。条件は `cargo` が使えること。回避策は `mdbook --version` と `cargo install mdbook` を先に明示すること。
- 2026-03-10 / TICKET-2026-03-10-004: sandbox や headless 環境では `mdbook serve --open` が localhost bind やブラウザ起動で失敗しうる。条件は制限付き実行環境。回避策は `mdbook build` を最低確認に置き、`serve --open` はローカル端末で試すこと。
- 2026-03-10 / TICKET-2026-03-10-004: `serve --open` の成功だけではブラウザ画面そのものの記録は残らない。条件は CLI ベースの確認のみで進める場合。回避策は必要なら後続 block で画面キャプチャを別途回収すること。

## Template
- 日付:
- ticket / block:
- gotcha:
- condition:
- workaround:
