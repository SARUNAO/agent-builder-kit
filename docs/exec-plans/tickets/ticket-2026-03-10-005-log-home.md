---
ticket_id: TICKET-2026-03-10-005
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-003
title: 一次記録 docs の置き場と index を作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - docs/exec-plans/active/index.md
  - docs/exec-plans/active/
lane_order: 100
depends_on: TICKET-2026-03-10-004
kind: ticket
---

# 一次記録 docs の置き場と index を作る

- ticket_id: TICKET-2026-03-10-005
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-003
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- decision / gotcha / command / before-after を残す docs の置き場を作り、active index から辿れるようにする

## やること
- `docs/exec-plans/active/` 配下に、記録用 docs を追加する
- `docs/exec-plans/active/index.md` から辿れるようにする
- 各 docs は本文ではなく一次記録の置き場であることを明記する

## やらないこと
- 実例ログの本格記入
- mdBook 本文への組み込み
- GitHub 公開向けの整形

## Editable Paths
- `docs/exec-plans/active/index.md`
- `docs/exec-plans/active/`

## Inputs
- `docs/exec-plans/blocks/block-007-process-logging.md`
- BLK-002 の返却物方針

## Implementation Notes
- 置き場は `docs/exec-plans/active/` に寄せる
- raw 過ぎる情報は避け、再現に必要な最小限の事実を残す前提で見出しを切る

## Verification
- active index から記録 docs へ辿れる
- 各 docs の役割が見出しだけで分かる

## Done When
- 記録のホームができ、後続 ticket が迷わず追記できる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 置き場の粒度と導線が過不足ないか

## 完了時に返すもの
- `fact-report`
- 作成した記録 docs の一覧
- 運用時の注意点

## 実施結果
- `docs/exec-plans/active/index.md` を更新し、一次記録 docs の入口を追加した
- `decision-log.md`, `gotcha-log.md`, `command-log.md`, `before-after.md` を新規作成した
- 各 docs に「これは本文ではなく一次記録の置き場である」ことと、追記粒度の目安を明記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- active index から 4 種の記録 docs へ辿れる状態にした
- 各 docs が decision / gotcha / command / before-after の役割を見出しだけで説明していることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-005-log-home.md`
