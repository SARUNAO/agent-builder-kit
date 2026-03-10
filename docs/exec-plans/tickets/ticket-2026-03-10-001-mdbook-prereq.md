---
ticket_id: TICKET-2026-03-10-001
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-001
title: mdBook 導入前提と初回コマンドを整理する
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - README.md
  - docs/HUMAN_MANUAL.md
lane_order: 100
depends_on: "-"
kind: ticket
---

# mdBook 導入前提と初回コマンドを整理する

- ticket_id: TICKET-2026-03-10-001
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-001
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `mdbook` を知らない利用者でも、何を入れて最初に何を実行すればよいか分かる入口を作る

## やること
- `README.md` に mdBook 導入前提と最初の実行コマンド候補を追記する
- 必要なら `docs/HUMAN_MANUAL.md` に「未導入なら block 2 で導入確認する」旨を短く残す
- この環境で `mdbook` 未導入である事実を前提に、導入済み / 未導入の両ケースを迷わない文面にする

## やらないこと
- 実際の `mdbook` インストール自動化
- `book.toml` や `src/` の生成
- 公開設定や GitHub Actions の追加

## Editable Paths
- `README.md`
- `docs/HUMAN_MANUAL.md`

## Inputs
- `docs/exec-plans/blocks/block-002-mdbook-skeleton.md`
- `docs/exec-plans/discovery-brief.md`
- mdBook 公式の推奨フローとして `mdbook init` / `mdbook build` / `mdbook serve --open`

## Implementation Notes
- 文章は「mdBook を知らない利用者向け」を優先する
- コマンドは copy-paste しやすい最小セットに絞る
- この ticket は docs-only だが、後続 ticket がそのまま使う入口になる

## Verification
- 更新した docs を読み返して、未導入利用者が次に打つコマンドを 3 手以内で把握できること

## Done When
- `README.md` だけで mdBook 骨格作成の入口が分かる
- 必要なら `docs/HUMAN_MANUAL.md` に補足がある

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 初学者が読んで手順を誤解しないか

## 完了時に返すもの
- `fact-report`
- 更新した導入手順の要約
- 未導入環境で残る不明点
- decision / gotcha 候補のメモ

## 実施結果
- `README.md` に mdBook 初学者向けの入口、確認コマンド、導入コマンド、まだやらないことを追記した
- `docs/HUMAN_MANUAL.md` に mdBook 未導入時の扱いを追記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 更新後の docs を読み返し、未導入利用者が `cargo --version` -> `mdbook --version` -> `cargo install mdbook` の順で次アクションを把握できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-001-mdbook-prereq.md`
