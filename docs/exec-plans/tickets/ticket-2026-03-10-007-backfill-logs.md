---
ticket_id: TICKET-2026-03-10-007
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-004
title: BLK-002 の実例を decision / gotcha / command / before-after に落とす
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - docs/exec-plans/active/
  - docs/exec-plans/fact-reports/
lane_order: 100
depends_on: TICKET-2026-03-10-006
kind: ticket
---

# BLK-002 の実例を decision / gotcha / command / before-after に落とす

- ticket_id: TICKET-2026-03-10-007
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-004
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- BLK-002 の作業結果を、後で本文に再利用できる一次記録へ変換する

## やること
- BLK-002 の fact-report と返却物をもとに、decision / gotcha / command / before-after へ事実を書き出す
- 記録不足があれば、どこが足りないかを明記する
- 本文向けの解釈は最小限に留める

## やらないこと
- 章本文の執筆
- 新しい機能追加
- GitHub 公開設定の追加

## Editable Paths
- `docs/exec-plans/active/`
- `docs/exec-plans/fact-reports/`

## Inputs
- BLK-002 配下の fact-report
- BLK-002 配下 ticket の返却物
- TICKET-2026-03-10-005 / 006 で整えた記録ルール

## Implementation Notes
- 不明点は埋めずに「記録不足」として残す
- 事実と後知恵を混ぜない

## Verification
- 4 系統の記録のうち、BLK-002 で取得できるものが埋まっている
- 記録不足箇所が判別できる

## Done When
- BLK-002 を記事化するための一次記録が最低限揃う

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 記録が事実ベースに留まっているか

## 完了時に返すもの
- `fact-report`
- 追記した記録項目の要約
- 記録不足の一覧

## 実施結果
- BLK-002 配下の fact-report と README をもとに、`decision-log.md`, `gotcha-log.md`, `command-log.md`, `before-after.md` へ retro 収集を行った
- 4 系統それぞれに、後続の本文で再利用しやすい短い事実を追記した
- 記録不足として、ブラウザ画面キャプチャや `cargo install mdbook` の所要時間は回収できていないことを明記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 4 系統の active logs すべてに BLK-002 の実例を追加した
- decision / gotcha / command / before-after の各項目が BLK-002 の fact-report と矛盾しないことを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-007-backfill-logs.md`
