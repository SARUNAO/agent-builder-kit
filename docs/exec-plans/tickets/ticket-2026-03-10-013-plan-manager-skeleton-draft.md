---
ticket_id: TICKET-2026-03-10-013
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-007
title: `plan-manager でプロジェクトの骨子を組む` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/plan-manager-skeleton.md
  - src/SUMMARY.md
lane_order: 100
depends_on: TICKET-2026-03-10-012
kind: ticket
---

# `plan-manager でプロジェクトの骨子を組む` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-013
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-007
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `plan-manager-skeleton.md` を、`plan-manager` が project の骨子を組む章ドラフトへ育てる

## やること
- `plan-manager` が最初に何を読み、何を決めるかを説明する
- `project-intake`, `discovery-brief`, `plan-spec`, block note の役割を短く整理する
- 必要なら `src/SUMMARY.md` の章ラベルも本文に合わせて調整する
- 本文の流れに応じて章タイトル変更案があれば残す

## Editable Paths
- `src/plan-manager-skeleton.md`
- `src/SUMMARY.md`

## Verification
- 章単体で読んでも、`plan-manager` が project の骨子を組む流れが分かる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/SUMMARY.md` の章ラベルを `plan-manager でプロジェクトの骨子を組む` に変更した
- `src/plan-manager-skeleton.md` を、`plan-manager` の役割と使い方を説明する草稿へ差し替えた
- `plan-manager` が何を読み、何を作り、どう使うかを最低限追える構成にした
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 章単体で読んでも、`plan-manager` の役割と入口の使い方が分かる状態になった
- `mdbook build` が成功し、章ラベル変更後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-013-plan-manager-skeleton-draft.md`
