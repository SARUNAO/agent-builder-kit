---
ticket_id: TICKET-2026-03-10-003
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-002
title: 初期の章ファイルと `SUMMARY.md` を整える
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/SUMMARY.md
  - src/**/*.md
lane_order: 100
depends_on: TICKET-2026-03-10-002
kind: ticket
---

# 初期の章ファイルと `SUMMARY.md` を整える

- ticket_id: TICKET-2026-03-10-003
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-002
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- 後続の本文執筆に使える最小章構成を `src/` に仮置きする

## やること
- `src/SUMMARY.md` に 4 章前後の最小構成を定義する
- 各章に対応する markdown ファイルを作る
- 本文は見出しと短い案内程度に留め、BLK-003 で膨らませやすい状態にする

## やらないこと
- ワークショップ本文の詳細化
- GitHub 公開向けの装飾
- 章を増やしすぎること

## Editable Paths
- `src/SUMMARY.md`
- `src/**/*.md`

## Inputs
- `docs/exec-plans/blocks/block-003-workshop-content.md`
- TICKET-2026-03-10-002 で生成した `src/`

## Implementation Notes
- 章タイトルは日本語でよい
- 候補は「概要」「環境確認」「role フロー体験」「最初の変更」を基準にする
- 章内目次で将来拡張できるよう、構造を単純に保つ

## Verification
- `src/SUMMARY.md` のリンク先がすべて存在する
- 4 章前後の構成が `BLK-003` の起点として読める

## Done When
- 最小章構成が repo に入り、BLK-003 が本文執筆へ進める

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] reviewer からの承認、または重大 findings 解消済みを確認した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: `SUMMARY.md` と章ファイルの対応が崩れていないか

## 完了時に返すもの
- `fact-report`
- 作成した章ファイル一覧
- 章タイトル案
- 未解決事項
- before / after と article source 候補のメモ

## 実施結果
- `src/SUMMARY.md` を 4 章構成へ更新した
- `src/overview.md` を最小スタブとして残しつつ、`src/environment-check.md`, `src/role-flow.md`, `src/first-change.md` を追加した
- 各章は BLK-003 で本文を膨らませやすいよう、見出しと短い案内に留めた
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `src/SUMMARY.md` に列挙した 4 つのリンク先ファイルがすべて存在することを確認した
- 章構成が「概要」「環境確認」「role フロー体験」「最初の変更」の 4 章になっていることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-003-summary-and-stubs.md`
