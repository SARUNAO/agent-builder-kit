---
ticket_id: TICKET-2026-03-10-032
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-016
title: 公開後確認と未実施チェックの整理を行う
status: pending
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - README.md
  - docs/HUMAN_MANUAL.md
  - docs/exec-plans/active/attention-queue.md
lane_order: 200
depends_on: TICKET-2026-03-10-031
kind: ticket
---

# 公開後確認と未実施チェックの整理を行う

- ticket_id: TICKET-2026-03-10-032
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-016
- status: pending
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- 公開後に見えた確認項目と、まだ未実施の品質チェックを整理する

## やること
- 公開後の最低限の確認結果をまとめる
- link check や追加 lint を後続改善として切り分ける
- README / Human Manual の公開後手順を調整する

## Editable Paths
- `README.md`
- `docs/HUMAN_MANUAL.md`
- `docs/exec-plans/active/attention-queue.md`

## Verification
- 公開達成と残課題が docs 上で混同されていない

## Done チェック
- [ ] Goal を満たす更新が入っている
- [ ] Verification を実施して結果を残した
- [ ] docs-only skip または reviewer sign-off の扱いを明記した
- [ ] 未解決事項があれば `fact-report` に記録した
