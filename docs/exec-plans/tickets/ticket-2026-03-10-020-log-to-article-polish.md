---
ticket_id: TICKET-2026-03-10-020
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-010
title: `開発ログからチュートリアル本文を組み立てる` 章の推敲と根拠同期を行う
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/process-to-article.md
  - src/SUMMARY.md
  - docs/exec-plans/active/article-source-map.md
lane_order: 200
depends_on: TICKET-2026-03-10-019
kind: ticket
---

# `開発ログからチュートリアル本文を組み立てる` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-020
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-010
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- `process-to-article.md` の本文を推敲し、記録 docs と本文の根拠導線を整理する

## やること
- 本文推敲を反映する
- 必要なら article source map の章名と章意図を同期する
- 章タイトルを変えた場合は本文、`src/SUMMARY.md`、source map の表記をそろえる

## Editable Paths
- `src/process-to-article.md`
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
- `src/process-to-article.md` の文面を少しやわらかく推敲し、この章が AI エージェント側の提案で立てられ、人間が採用した章であることを本文へ追記した
- `docs/exec-plans/active/article-source-map.md` に `開発ログからチュートリアル本文を組み立てる` 章を追加し、章意図と根拠を同期した
- planning docs、active logs、fact-report の役割分担が本文と source map で一致するよう整えた
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 本文と source map の章意図が、記録から本文へ変換する章として一致した
- `mdbook build` が成功し、推敲後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-020-log-to-article-polish.md`
