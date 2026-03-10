---
ticket_id: TICKET-2026-03-10-021
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-011
title: `真のハーネスエンジニアリングへ至るには？` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/true-harness-engineering.md
  - src/SUMMARY.md
lane_order: 100
depends_on: TICKET-2026-03-10-020
kind: ticket
---

# `真のハーネスエンジニアリングへ至るには？` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-021
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-011
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `true-harness-engineering.md` を、現状の限界と拡張余地を整理する本文ドラフトへ育てる

## やること
- 現在の `agent-builder-kit` で不足している点を整理する
- マルチエージェント化や並列実行の方向性を説明する
- CI/CD や境界可視化、レイヤードアーキテクチャ支援 Skill などの拡張案を説明する
- 必要なら `src/SUMMARY.md` の章ラベルも本文に合わせて調整する

## Editable Paths
- `src/true-harness-engineering.md`
- `src/SUMMARY.md`

## Verification
- 章単体で読んでも、現状課題と拡張方針の両方が追える

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `src/true-harness-engineering.md` を新規作成し、現状の到達点、限界、拡張候補を整理する草稿を追加した
- `src/SUMMARY.md` に `真のハーネスエンジニアリングへ至るには？` 章を追加した
- OpenAI の harness engineering 記事を参照し、評価・足場・運用設計を含む観点を本文へ反映した
- CI/CD やレイヤードアーキテクチャ支援を kit に標準同梱していない理由として、「プロジェクト依存が強く、汎用性を優先した」旨を注記した
- Rust の Clippy を例に、リンターや static analysis も有効だが kit の標準範囲外であることを追記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `mdbook build` を実行し、新章追加後も book が生成できることを確認した
- `src/SUMMARY.md` から `src/true-harness-engineering.md` が参照されることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-021-true-harness-engineering-draft.md`
