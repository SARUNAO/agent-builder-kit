---
ticket_id: TICKET-2026-03-10-029
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-015
title: README と補助 docs に GitHub 公開導線を追加する
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - README.md
  - docs/HUMAN_MANUAL.md
lane_order: 100
depends_on: TICKET-2026-03-10-028
kind: ticket
---

# README と補助 docs に GitHub 公開導線を追加する

- ticket_id: TICKET-2026-03-10-029
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-015
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- README と補助 docs から GitHub 公開 site と repo 構成が追えるようにする

## やること
- README に公開導線と repo 構造の説明を追加する
- `agent-builder-kit` と mdBook が同一 repo にある前提を補助 docs へ反映する
- 公開 URL 未確定なら placeholder と差し替えポイントを残す

## Editable Paths
- `README.md`
- `docs/HUMAN_MANUAL.md`

## Verification
- 公開 site と repo の関係が docs から追える

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `README.md` に GitHub Pages の公開導線 placeholder と、同一 repo で mdBook / `agent-builder-kit` を併置している説明を追加した
- `docs/HUMAN_MANUAL.md` に、GitHub 公開時に人間が判断することを追記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- README から公開 site placeholder と repo 構造の関係を追えることを確認した
- Human Manual から、初回 publish 後に人間が何を判断するかが読めることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-029-publish-docs-links.md`
