# Gap Report Template

既存運用を新しい schema へ移すときの差分を整理する docs。  
`project-inventory` のあとに作成し、どこがそのまま流用できて、どこが移行対象かを明示する。

```md
# Gap Report: {project name}

- gap_report_id: GAP-YYYY-MM-DD-XXX
- related_plan: PLAN-YYYY-MM-DD-XXX
- status: in_progress
- owner: プランオーナー
- last_updated: YYYY-MM-DD

## 移行目的
- なぜこの migration を行うか
- 成功したとき何が揃っているべきか

## Mapping Summary
| current_item | target_item | gap_type | required_action | owner | notes |
|---|---|---|---|---|---|
| docs/foo.md | docs/PRODUCT_SENSE.md | partial | 要約して統合 | plan-owner | 文脈は維持する |

## 高リスク差分
- source of truth が曖昧
- 既存 docs が複数に散っている
- 現行 AI の暗黙知に依存している

## 人間確認が必要な判断
- 削除してよい docs
- 移行後の正本 path
- 既存 issue / board の扱い

## 次アクション
- `adoption-plan` にフェーズ化する
```
