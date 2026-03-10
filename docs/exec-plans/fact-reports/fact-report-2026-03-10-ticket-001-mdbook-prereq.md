# Fact Report: mdBook 導入前提と初回コマンドを整理する

- ticket_id: TICKET-2026-03-10-001
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `README.md`
- `docs/HUMAN_MANUAL.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-001-mdbook-prereq.md`

## 実行したコマンド
- `sed -n '1,260p' README.md`
- `sed -n '1,260p' docs/HUMAN_MANUAL.md`
- `rg -n "mdBook|mdbook|cargo install mdbook|mdbook --version" README.md docs/HUMAN_MANUAL.md`

## 結果
- `README.md` に mdBook 初学者向けの入口と、最初に見るべきコマンドを追記した
- `docs/HUMAN_MANUAL.md` に `mdbook` 未導入時の扱いを追記した
- この環境で `mdbook` 未導入でも、次 ticket で何を確認すべきか分かる入口を作った

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `cargo install mdbook` をこの環境で実行していないため、実際の導入所要時間やエラーの有無は未確認
- `mdbook init` を repo root でどう適用するかは次 ticket で確定する

## scope breach
- なし

## 補足
- decision 候補: 初学者向け入口は `README.md` に集約する
- gotcha 候補: `mdbook` 未導入でも block を止めず、まず確認コマンドを明示する
- 次 ticket に渡すべき事実: 現時点では導入前提の説明のみ整備済みで、`book.toml` と `src/` はまだ存在しない
