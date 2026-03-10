---
ticket_id: TICKET-2026-03-10-030
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-015
title: 本文と公開導線の表現を同期する
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/overview.md
  - src/conclusion.md
  - docs/exec-plans/active/article-source-map.md
lane_order: 200
depends_on: TICKET-2026-03-10-029
kind: ticket
---

# 本文と公開導線の表現を同期する

- ticket_id: TICKET-2026-03-10-030
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-015
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- 本文側にも公開導線の表現を同期し、読者の導線を閉じる

## やること
- `overview` や `conclusion` の公開前 placeholder を現状に合わせて見直す
- 必要なら article source map の根拠や足りない記録を更新する
- 同一 repo 公開前提と矛盾しないよう本文を整える

## Editable Paths
- `src/overview.md`
- `src/conclusion.md`
- `docs/exec-plans/active/article-source-map.md`

## Verification
- README と本文の公開導線が矛盾していない

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/overview.md` の公開前 placeholder を、同一 repo 公開前提が分かる表現へ整えた
- `src/conclusion.md` に、公開後は tutorial site と `agent-builder-kit` を同一 repo で行き来できる旨を追記した
- `docs/exec-plans/active/article-source-map.md` に公開導線の根拠を追加した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- README と本文の公開導線が、同一 repo + project Pages 前提で矛盾していないことを確認した
- source map の章意図と本文の公開導線が矛盾していないことを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-030-publish-docs-polish.md`
