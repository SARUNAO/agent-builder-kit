---
ticket_id: TICKET-2026-03-10-010
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-005
title: 既存 4 章の導入文を `agent-builder-kit` 主軸へ寄せる
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/overview.md
  - src/plan-manager-skeleton.md
  - src/role-flow.md
  - src/first-change.md
lane_order: 200
depends_on: TICKET-2026-03-10-009
kind: ticket
---

# 既存 4 章の導入文を `agent-builder-kit` 主軸へ寄せる

- ticket_id: TICKET-2026-03-10-010
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-005
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- 既存 4 章の導入文が、mdBook 中心ではなく `agent-builder-kit` tutorial の流れとして読める状態にする

## やること
- `overview.md`, `plan-manager-skeleton.md`, `role-flow.md`, `first-change.md` の冒頭文を見直す
- 各章が「mdBook の一般解説」ではなく「この開発フローで何を見せる章か」になっているかを揃える
- 必要なら `article-source-map.md` と矛盾しないよう表現を寄せる

## やらないこと
- 各章の本文を大きく書き足すこと
- 新しい章の追加
- 公開向けデザイン調整

## Editable Paths
- `src/overview.md`
- `src/plan-manager-skeleton.md`
- `src/role-flow.md`
- `src/first-change.md`

## Inputs
- TICKET-2026-03-10-009 で追加した導入章
- `docs/exec-plans/active/article-source-map.md`

## Implementation Notes
- 文体はやわらかくしてよいが、章の役割は曖昧にしない
- 章ごとの根拠は article source map と矛盾させない

## Verification
- 4 章の冒頭だけを読んでも、`agent-builder-kit` tutorial の流れとしてつながる
- mdBook の一般入門に見えすぎる文が減っている

## Done When
- BLK-003 の主題配分 3:7 に沿う章の入口が揃っている

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 各章の冒頭が主題シフトと矛盾していないか

## 完了時に返すもの
- `fact-report`
- 更新した章冒頭の一覧
- まだ mdBook 入門寄りに見える箇所のメモ

## 実施結果
- `overview.md` を、「はじめに」の次に読む `agent-builder-kit` の導入編として読める表現へ寄せた
- `src/SUMMARY.md` と `overview.md` の章ラベルも `agent-builder-kit の導入` にそろえた
- `plan-manager-skeleton.md`, `role-flow.md`, `first-change.md` の冒頭を、mdBook 一般入門ではなく、この開発フローの各段階として読めるよう調整した
- 人間コメントを踏まえ、次章の導線は「agent-builder-kit の導入」寄りに整理した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 4 章の冒頭を通して読むと、「導入 -> 足場確認 -> role フロー -> 最初の変更」という tutorial の流れになることを確認した
- mdBook 単体の一般入門に見える表現を減らし、`agent-builder-kit` の運用に重心を寄せた
- 章一覧でも `概要` ではなく `agent-builder-kit の導入` と表示されるようになった

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-010-reframe-existing-chapters.md`
