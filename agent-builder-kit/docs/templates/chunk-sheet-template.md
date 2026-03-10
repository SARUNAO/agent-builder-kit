# Chunk Sheet Template

plan を 2-5 task 程度に分割した中間単位。  
`タスクプランナー` が管理する。

```md
---
chunk_id: CHUNK-YYYY-MM-DD-XXX
parent_plan: PLAN-YYYY-MM-DD-XXX
parent_block: BLK-XXX
status: pending
owner: タスクプランナー
last_updated: YYYY-MM-DD
title: {chunk title}
kind: chunk
---

# {chunk title}

- chunk_id: CHUNK-YYYY-MM-DD-XXX
- parent_plan: PLAN-YYYY-MM-DD-XXX
- parent_block: BLK-XXX
- status: pending
- owner: タスクプランナー
- last_updated: YYYY-MM-DD

## chunk の目的
- このまとまりで達成したいこと

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-001 | 例 | タスクワーカー | pending | `src/foo`, `tests/foo` | - |

## 完了条件
- 含まれる ticket がすべて review 通過済み
- chunk review の重大 findings がない
- docs sync 対象が整理済み

## Done チェック
- [ ] 含まれる ticket がすべて `done`
- [ ] chunk review の重大 findings が解消済み
- [ ] docs / status 更新が完了している
- [ ] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- 並列にしてよい ticket
- 同時編集禁止の境界

## 統合時の注意
- task 間の接続点
- 命名や型の整合
- 後続 chunk への影響

## chunk review 観点
- 統合確認項目
- docs 更新が必要になりやすい箇所

## 進捗メモ
- YYYY-MM-DD: 更新内容
```
