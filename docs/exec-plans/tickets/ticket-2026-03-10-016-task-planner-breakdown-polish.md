---
ticket_id: TICKET-2026-03-10-016
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-008
title: `task-planner で仕事を chunk と ticket に分ける` 章の推敲と根拠同期を行う
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/role-flow.md
  - src/SUMMARY.md
  - docs/exec-plans/active/article-source-map.md
lane_order: 200
depends_on: TICKET-2026-03-10-015
kind: ticket
---

# `task-planner で仕事を chunk と ticket に分ける` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-016
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-008
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- `role-flow.md` の本文を推敲し、`task-planner` の分解判断と根拠導線を整理する

## やること
- 本文推敲を反映する
- 必要なら article source map の章名と章意図を同期する
- 章タイトルを変えた場合は本文、`src/SUMMARY.md`、source map の表記をそろえる

## Editable Paths
- `src/role-flow.md`
- `src/SUMMARY.md`
- `docs/exec-plans/active/article-source-map.md`

## Verification
- 本文と source map の章意図が一次記録と矛盾していない

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/role-flow.md` の表記ゆれと typo を整え、図版キャプションまわりの文面を読みやすく推敲した
- `docs/exec-plans/active/article-source-map.md` の旧章名 `role フロー体験` を、現行の `task-planner で仕事を chunk と ticket に分ける` へ同期した
- `planner_chunk2.png` を含む現行の図版構成と、章意図・根拠を source map 側へ反映した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 本文と source map の章意図が、`task-planner` の役割、分解、再計画判断を扱う章として一致した
- `mdbook build` が成功し、推敲後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-016-task-planner-breakdown-polish.md`
