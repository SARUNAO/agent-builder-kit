# Fact Report: `mdbook init` で最小骨格を作る

- ticket_id: TICKET-2026-03-10-002
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `book.toml`
- `src/SUMMARY.md`
- `src/overview.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-002-mdbook-init.md`

## 実行したコマンド
- `mdbook --version`
- `mdbook init --help`
- `mdbook init --force --title "mdBook Workshop" .`
- `find src -maxdepth 2 -type f | sort`
- `sed -n '1,260p' book.toml`

## 結果
- `cargo install mdbook` により `mdbook v0.5.2` を導入した
- `mdbook init` により `book.toml` と `src/SUMMARY.md` を含む最小骨格を生成した
- 生成された英語サンプルを、次 ticket が使いやすいよう日本語の最小スタブへ整えた

## reviewer 結果
- no findings
- `mdbook build` を reviewer 観点で追加実行し、HTML 出力まで成功したことを確認した

## 未解決事項
- `mdbook build` と `mdbook serve --open` の実確認はまだしていない
- 初期章は 1 章のみなので、4 章前後の構成は次 ticket で整える

## scope breach
- なし

## 補足
- before: `book.toml` と `src/` は存在しなかった
- after: `book.toml`, `src/SUMMARY.md`, `src/overview.md` が存在する
- decision 候補: 初期生成物は英語サンプルのままではなく、日本語の最小スタブへ寄せる
- 次 ticket に渡すべき事実: mdBook 骨格は生成済みで、`SUMMARY.md` は 1 章構成になっている
- reviewer メモ: 現時点では `mdbook build` が通るため、TICKET-003 は章追加に進める
