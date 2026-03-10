---
ticket_id: TICKET-2026-03-10-015
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-008
title: `task-planner で仕事を chunk と ticket に分ける` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/role-flow.md
  - src/SUMMARY.md
lane_order: 100
depends_on: TICKET-2026-03-10-014
kind: ticket
---

# `task-planner で仕事を chunk と ticket に分ける` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-015
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-008
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `role-flow.md` を、`task-planner` が仕事を chunk / ticket に分解する本文ドラフトへ育てる

## やること
- `task-planner` が何を読み、何を生成するかを説明する
- block から chunk / ticket へ落とす考え方を説明する
- 必要なら `src/SUMMARY.md` の章ラベルも本文に合わせて調整する
- 本文の流れに応じて章タイトル変更案があれば残す

## Editable Paths
- `src/role-flow.md`
- `src/SUMMARY.md`

## Verification
- 章単体で読んでも、block -> chunk -> ticket への分解が追える

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/role-flow.md` を、`task-planner` の役割、使い方、chunk / ticket への分解基準を説明する草稿へ差し替えた
- `src/SUMMARY.md` の章ラベルを `task-planner で仕事を chunk と ticket に分ける` に更新した
- 実例として `BLK-002` を `CHUNK-001`, `CHUNK-002` と `TICKET-001` から `TICKET-004` に分解した流れを章内へ取り込んだ
- ticket 完了後に chunk を差し込み更新する判断と、block 単位へ戻す判断の違いを追記した
- `src/images/before_chunk.png`, `src/images/after_chunk.png` を更新前後の図として本文へ組み込んだ
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `mdbook build` を実行し、章ラベル変更と本文差し替え後も book が生成できることを確認した
- `src/SUMMARY.md` から `src/role-flow.md` が新章タイトルで参照されることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-015-task-planner-breakdown-draft.md`
