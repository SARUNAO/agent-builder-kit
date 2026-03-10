# Project Inventory Template

既存プロジェクトの docs、運用、受け渡し境界を棚卸しする docs。  
標準では `プランオーナー` が主担当で、現行 AI に初回ドラフトを依頼してよい。

```md
# Project Inventory: {project name}

- inventory_id: INVENTORY-YYYY-MM-DD-XXX
- related_plan: PLAN-YYYY-MM-DD-XXX
- status: in_progress
- owner: プランオーナー
- last_updated: YYYY-MM-DD

## 現在の運用要約
- いま何を source of truth としているか
- どの docs / issue / チャットが実質の受け渡しになっているか
- block / chunk / ticket 相当の単位が何か

## 既存 docs / artefact 棚卸し
| path_or_location | kind | current_role | keep_or_replace | notes |
|---|---|---|---|---|
| docs/foo.md | spec | plan-owner 相当 | keep | 現行の正本 |

## 現在の flow mapping
| current_unit | observed_meaning | target_schema | notes |
|---|---|---|---|
| Epic A | 大きい開発単位 | block | 1:1 で写像できそう |

## 保護すべきもの
- 失うと困る docs
- すぐには動かせない path
- 人間判断なしで変えない運用

## 未把握事項
- AI だけでは確定できない点
- 人間確認が必要な点

## 次アクション
- `gap-report` を更新する
- `adoption-plan` のフェーズを切る
```
