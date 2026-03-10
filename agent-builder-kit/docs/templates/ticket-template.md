# Ticket Template

タスクワーカーに渡す契約書。  
1 ticket = 1 ワーカー所有を基本とする。

```md
---
ticket_id: TICKET-YYYY-MM-DD-XXX
parent_plan: PLAN-YYYY-MM-DD-XXX
parent_chunk: CHUNK-YYYY-MM-DD-XXX
status: pending
owner: タスクプランナー
assignee: タスクワーカー
lane_order: 100
last_updated: YYYY-MM-DD
title: {ticket title}
kind: ticket
---

# {ticket title}

- ticket_id: TICKET-YYYY-MM-DD-XXX
- parent_plan: PLAN-YYYY-MM-DD-XXX
- parent_chunk: CHUNK-YYYY-MM-DD-XXX
- status: pending
- owner: タスクプランナー
- assignee: タスクワーカー
- lane_order: 100
- last_updated: YYYY-MM-DD

## Goal
- 今回達成すること

## やること
- 項目 1
- 項目 2

## やらないこと
- 項目 1
- 項目 2

## Editable Paths
- `path/to/file`

## Inputs
- 参照 docs
- 依存 ticket
- 前提条件

## Implementation Notes
- 実装時の注意
- 既知の地雷

## Verification
- 実行すべきコマンド
- 省略可の確認と理由

## Done When
- 条件 1
- 条件 2

## Done チェック
- [ ] Goal を満たす実装が入っている
- [ ] Verification を実施して結果を残した
- [ ] reviewer からの承認、または重大 findings 解消済みを確認した
- [ ] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill:
- reviewer に見てほしい観点:

## 完了時に返すもの
- `fact-report`
- 実行コマンド
- テスト結果
- 未解決事項
```
