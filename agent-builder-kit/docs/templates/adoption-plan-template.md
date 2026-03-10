# Adoption Plan Template

移行を一括で行わず、段階的に定着させるための docs。  
`gap-report` を元に、どの順で置き換えと併用を進めるかを定義する。

```md
# Adoption Plan: {project name}

- adoption_plan_id: ADOPT-YYYY-MM-DD-XXX
- related_plan: PLAN-YYYY-MM-DD-XXX
- status: pending
- owner: プランオーナー
- last_updated: YYYY-MM-DD

## 目的
- 新 schema へ安全に移行する
- 既存運用の停止時間を最小にする

## フェーズ
| phase | goal | scope | exit_criteria | owner |
|---|---|---|---|---|
| 1 | 棚卸し完了 | inventory / gap-report | current docs の mapping が埋まる | plan-owner |
| 2 | 正本の仮設置 | core docs | AGENTS と docs/ の正本が決まる | plan-owner |
| 3 | planning 置き換え | block / chunk / ticket | task 化が新 schema で回る | task-planner |
| 4 | 可視化同期 | canvas / references | 可視化と docs が同期する | task-planner |

## 並行運用ルール
- 旧 docs をすぐ削除しない
- 移行完了まで source of truth の暫定ルールを明記する
- 人間承認前に破壊的な rename / move をしない

## ブロッカー
- path 保護
- 現行 AI の暗黙知
- 人間承認待ち

## 完了条件
- 正本 docs が新 schema に揃う
- role ごとの責務が切り替わる
- 旧運用の参照が整理される
```
