---
ticket_id: TICKET-2026-03-10-018
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-009
title: `task-worker で ticket を実行し、fact-report を返す` 章の推敲と根拠同期を行う
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/first-change.md
  - src/SUMMARY.md
  - docs/exec-plans/active/article-source-map.md
lane_order: 200
depends_on: TICKET-2026-03-10-017
kind: ticket
---

# `task-worker で ticket を実行し、fact-report を返す` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-018
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-009
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- `first-change.md` の本文を推敲し、`task-worker` の実行結果と根拠導線を読者向けに整理する

## やること
- 本文推敲を反映する
- ticket 完了後に上流へ結果を返し、status を昇華させる流れを章内へ追加する
- 必要なら article source map の章名と章意図を同期する
- 章タイトルを変えた場合は本文、`src/SUMMARY.md`、source map の表記をそろえる

## Editable Paths
- `src/first-change.md`
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
- `src/first-change.md` の文面を推敲し、`task-worker` の責務、`fact-report` の価値、reviewer handoff の切り分けを読みやすく整えた
- ticket 完了後に `task-planner` と `plan-manager` へ結果が返り、status が昇華する流れを章内へ追加した
- `docs/exec-plans/active/article-source-map.md` の旧章名 `最初の変更` を、現行の `task-worker で ticket を実行し、fact-report を返す` へ同期した
- `TICKET-017` の草稿内容と現行本文に合わせて、source map の章意図と根拠を更新した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 本文と source map の章意図が、`task-worker` の実行、返却、reviewer handoff を扱う章として一致した
- `task-worker -> task-planner -> plan-manager` の status 昇華フローが本文に追加され、運用 schema と矛盾しないことを確認した
- `mdbook build` が成功し、推敲後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-018-task-worker-execution-polish.md`

## プランナー裁定メモ
- 2026-03-10: 利用者から「ticket 完了後に上流へ結果を流し、status を昇華させる節が欠けている」と追加要望が入った
- この追加は現 chapter の射程に収まるため、新 block へは戻さず TICKET-018 の残作業として継続する
