---
ticket_id: TICKET-2026-03-10-008
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-004
title: 記録から記事素材マップを作る
status: pending
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - docs/exec-plans/active/
  - src/
lane_order: 200
depends_on: TICKET-2026-03-10-007
kind: ticket
---

# 記録から記事素材マップを作る

- ticket_id: TICKET-2026-03-10-008
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-004
- status: pending
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- どの記録を、どの章や節の根拠に使うかを一覧化する

## やること
- decision / gotcha / command / before-after の各記録を章候補へマッピングする
- `src/` 側へ直接本文を書き込みすぎず、素材マップとして残す
- BLK-003 の章作成 ticket が参照できるように整理する

## やらないこと
- 章本文の本格執筆
- 記録内容の改変
- 公開設定の追加

## Editable Paths
- `docs/exec-plans/active/`
- `src/`

## Inputs
- TICKET-2026-03-10-007 で埋めた一次記録
- `docs/exec-plans/blocks/block-003-workshop-content.md`

## Implementation Notes
- 素材マップは「章 / 根拠 / 足りない記録」が一目で分かる形にする
- BLK-003 で構成変更しやすいよう、結合度を上げすぎない

## Verification
- 少なくとも初期 4 章に対して根拠候補が紐づいている
- BLK-003 の worker が次に読むべき記録を見失わない

## Done When
- BLK-003 が一次記録を根拠に本文作成へ進める

## Done チェック
- [ ] Goal を満たす更新が入っている
- [ ] Verification を実施して結果を残した
- [ ] docs-only skip または reviewer sign-off の扱いを明記した
- [ ] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 素材マップが BLK-003 の入力として十分か

## 完了時に返すもの
- `fact-report`
- 章と根拠の対応表
- 足りない記録の一覧
