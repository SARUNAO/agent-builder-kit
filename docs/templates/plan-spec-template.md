# Plan Spec Template

曖昧な要求を仕様へ落とし込む中規模 docs。  
標準では `プランオーナー`、拡張時は `仕様設計者` が主担当。

```md
# {plan title}

- plan_id: PLAN-YYYY-MM-DD-XXX
- status: drafting
- owner: プランオーナー
- priority: high | medium | low
- last_updated: YYYY-MM-DD
- source_intake: INTAKE-YYYY-MM-DD-XXX
- source_discovery: DISCOVERY-YYYY-MM-DD-XXX

## 背景
- なぜ今やるか
- 現状の問題

## 目的
- この plan で達成する状態

## 非目的
- 今回やらないこと

## 成功条件
- 条件 1
- 条件 2
- 条件 3

## 制約
- 技術制約
- 運用制約
- 互換性制約

## 人間要求から採用したもの
- 要求原文のうち、仕様へ反映した点

## 人間に確認して確定した事項
- 決定事項

## 仮置き前提
- 人間未確認だが、現時点で採用する前提

## 未確定事項
- 要確認項目

## MVP 範囲
- 最初の chunk 群で成立させる最小スコープ

## High-level blocks
| block_id | title | goal | status | depends_on |
|---|---|---|---|---|
| BLK-001 | 例 | この block が達成すること | pending | - |

## 実装前提
- 着手前に必要な準備
- 依存する他 plan

## 参照先
- 関連 docs
- 関連コード

## 推奨分解方針
- 想定 chunk 数
- 並列化の可否
- 分けるときの境界

## 引き継ぎメモ
- `タスクプランナー` が task 化するときの注意
```
