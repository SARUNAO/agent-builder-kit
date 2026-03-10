# mdBook Workshop

AI コーディング前提の開発フローを運用するための docs 駆動 workspace。

## mdBook をまだ知らない人向け
- mdBook は、markdown ファイル群から書籍形式の静的サイトを作るためのツール
- この repo では、mdBook 自体を題材にしつつ、`plan-manager -> task-planner -> task-worker -> reviewer` の流れも教材化する
- 2026-03-10 時点でこの repo では `mdbook v0.5.2` を導入済み

## BLK-002 開始時の最小手順
1. Rust / Cargo が使えるか確認する: `cargo --version`
2. mdBook が入っているか確認する: `mdbook --version`
3. `mdbook` がなければ導入する: `cargo install mdbook`
4. 骨格生成フェーズに入ったら、repo root で `mdbook init` を使って最小構成を作る

## この段階で覚えておけばよいコマンド
- `mdbook --version`
- `mdbook init`
- `mdbook build`
- `mdbook serve --open`

## ローカル確認の最小手順
1. 生成確認だけなら repo root で `mdbook build` を実行する
2. 出力先は `book/` なので、build 成功後はそこに HTML が生成される
3. ブラウザ確認まで行うなら `mdbook serve --open` を実行する
4. `serve --open` が使いにくい環境では `mdbook serve` だけでもよい

## 2026-03-10 時点の確認結果
- `mdbook build` は成功し、`book/` に HTML を出力できた
- `mdbook serve --open` は通常のローカル環境では起動確認できた
- ただし Codex の sandbox では localhost bind が制限され、`Operation not permitted (os error 1)` で失敗することがある
- そのため、この repo の手順としては「ローカル端末で `mdbook serve --open` を試す」を正とする

## いまはまだやらないこと
- `book.toml` や `src/` の生成
- GitHub Pages 用の deploy 設定
- 章本文の本格執筆

## 最初に理解しておくこと
- init 後に `agent-builder-kit/` を削除した場合、展開元 package の docs や相対パスはもう前提にしない
- Codex アプリを再起動して project を開き直したあとの AI は、bootstrap 前や直前セッションの文脈を持っていない前提で扱う
- そのため、この repo の作業は毎回 `AGENTS.md` と `docs/` を読み直すところから始める

## Codex アプリでの再開手順
1. いまのスレッドを閉じる
2. Codex アプリを再起動する
3. この project を新しい project として開き直す
4. 新しいセッションの AI に、まず `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HUMAN_MANUAL.md` を読むよう依頼する
5. その後で `plan-manager` から作業を始める

## 入口
- `AGENTS.md`
- `docs/index.md`
- `docs/HUMAN_MANUAL.md`
- `docs/PLANS.md`
- `docs/ROLE_SKILLS.md`

## runtime artefact
- planning: `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks`
- canvas: `docs/exec-plans/canvas/development-flow.canvas`
- canonical skill source: `tools/codex-skills/`
- user-facing skill export: `.agents/skills/`

## 進め方
- `plan-manager` に目的と追加要件を伝える
- `task-planner` に chunk / ticket を切ってもらう
- `task-worker` と `reviewer` で実装と確認を進める
