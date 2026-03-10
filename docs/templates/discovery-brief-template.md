# Discovery Brief Template

曖昧な要求を仕様化可能な形へ整理する中間 docs。  
要求原文ではなく、確認済み事項と仮置き前提を分けて扱う。

```md
# Discovery Brief: {plan title}

- related_intake: INTAKE-YYYY-MM-DD-XXX
- related_plan: PLAN-YYYY-MM-DD-XXX
- status: drafting
- owner: プランオーナー
- last_updated: YYYY-MM-DD

## 要求の要約
- 原文を短く要約したもの

## 確定事項
- 人間が明示的に認めた事項

## 仮置き前提
- 現時点ではこう置く、という判断

## 未確定事項
- このままでは仕様固定できない論点

## block 着手前に詰める仕様
- block 名:
  - 未確定の実装判断
  - 人間へ確認したいこと
  - `plan-manager` のおすすめ案
  - 採用時の理由

## MVP 仮説
- 最小で成立する成果物

## 非目的
- 今回は含めないもの

## リスク
- 技術リスク
- データリスク
- 運用リスク

## 仕様化へ進める条件
- 何が決まれば `plan-spec` へ進めるか

## 人間へ返す確認事項
- 質問 1
- 質問 2

## 推奨案メモ
- `plan-manager` が提示する第一候補
- 代替案
- 迷った場合の判断基準
```
