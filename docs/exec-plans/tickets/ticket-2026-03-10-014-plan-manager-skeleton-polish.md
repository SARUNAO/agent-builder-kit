---
ticket_id: TICKET-2026-03-10-014
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-007
title: `plan-manager でプロジェクトの骨子を組む` 章の推敲と根拠同期を行う
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/plan-manager-skeleton.md
  - src/SUMMARY.md
  - docs/exec-plans/active/article-source-map.md
lane_order: 200
depends_on: TICKET-2026-03-10-013
kind: ticket
---

# `plan-manager でプロジェクトの骨子を組む` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-014
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-007
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- `plan-manager-skeleton.md` を推敲し、`plan-manager` の判断と根拠導線が伝わる章へ整える

## やること
- 本文推敲を反映する
- 必要なら article source map の章名と章意図を同期する
- 章タイトルを変えた場合は本文、`src/SUMMARY.md`、source map の表記をそろえる

## Editable Paths
- `src/plan-manager-skeleton.md`
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
- `plan-manager-skeleton.md` の表記ゆれとコードブロック表現を整え、読みやすい形へ推敲した
- `article-source-map.md` に TICKET-013 の fact-report と `.canvas` 補助アセットを追加し、章意図と根拠を同期した
- prompt 抜粋が本文に入ったため、source map 側の不足メモも更新した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 本文と source map の章意図が `plan-manager` の planning 行為を説明する章として一致した
- `mdbook build` が成功し、推敲後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-014-plan-manager-skeleton-polish.md`
