---
ticket_id: TICKET-2026-03-10-019
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-010
title: `開発ログからチュートリアル本文を組み立てる` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/process-to-article.md
  - src/SUMMARY.md
lane_order: 100
depends_on: TICKET-2026-03-10-018
kind: ticket
---

# `開発ログからチュートリアル本文を組み立てる` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-019
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-010
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `process-to-article.md` を、開発ログからチュートリアル本文を組み立てる章ドラフトへ育てる

## やること
- planning docs, fact-report, active logs の役割を整理する
- 事実と解釈をどう分けて本文へ持ち込むかを説明する
- 必要なら `src/SUMMARY.md` の章ラベルも本文に合わせて調整する

## Editable Paths
- `src/process-to-article.md`
- `src/SUMMARY.md`

## Verification
- 章単体で読んでも、記録から本文へ変換する流れが分かる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/process-to-article.md` を新規作成し、planning docs、fact-report、active logs をどう本文へ変換するかを説明する草稿を追加した
- `src/SUMMARY.md` に `開発ログからチュートリアル本文を組み立てる` 章を追加した
- `decision-log`, `gotcha-log`, `command-log`, `before-after`, `article-source-map` の役割分担を章内へ取り込んだ
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `mdbook build` を実行し、新章追加後も book が生成できることを確認した
- `src/SUMMARY.md` から `src/process-to-article.md` が参照されることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-019-log-to-article-draft.md`
