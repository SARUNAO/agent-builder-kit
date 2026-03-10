---
ticket_id: TICKET-2026-03-10-017
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-009
title: `task-worker で ticket を実行し、fact-report を返す` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/first-change.md
  - src/SUMMARY.md
lane_order: 100
depends_on: TICKET-2026-03-10-016
kind: ticket
---

# `task-worker で ticket を実行し、fact-report を返す` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-017
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-009
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `first-change.md` を、`task-worker` の実行と fact-report 返却が見える本文ドラフトへ育てる

## やること
- `task-worker` が ticket 単位で何をするかを説明する
- 実装結果を `fact-report` へ返す流れを説明する
- 必要なら reviewer handoff を章内の小見出しとして扱う
- 必要なら `src/SUMMARY.md` の章ラベルも本文に合わせて調整する
- 本文の流れに応じて章タイトル変更案があれば残す

## Editable Paths
- `src/first-change.md`
- `src/SUMMARY.md`

## Verification
- 章単体で読んでも、`task-worker` が何を実行し何を返すかが追える

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/first-change.md` を、`task-worker` の役割、ticket 実行、`fact-report` 返却、reviewer handoff を説明する草稿へ差し替えた
- `src/SUMMARY.md` の章ラベルを `task-worker で ticket を実行し、fact-report を返す` に更新した
- 実例として `TICKET-002` の `mdbook init` 実行と、`TICKET-004` の docs-only skip を章内へ取り込んだ
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `mdbook build` を実行し、章ラベル変更と本文差し替え後も book が生成できることを確認した
- `src/SUMMARY.md` から `src/first-change.md` が新章タイトルで参照されることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-017-task-worker-execution-draft.md`
