---
chunk_id: CHUNK-2026-03-10-016
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-004
title: 初回 publish と公開後確認を行う
status: pending
owner_role: task_planner
depends_on: CHUNK-2026-03-10-015
lane_order: 1600
kind: chunk
---

# 初回 publish と公開後確認を行う

- chunk_id: CHUNK-2026-03-10-016
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-004
- status: pending
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-015
- lane_order: 1600

## chunk の目的
- 初回 publish を実施し、公開後の最低限の確認を行う
- link check を後続改善へ回しつつ、公開達成の事実を残す

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-031 | GitHub Pages の初回 publish を実施して結果を記録する | task_worker | pending | `README.md`, `docs/exec-plans/active/attention-queue.md` | TICKET-2026-03-10-030 |
| TICKET-2026-03-10-032 | 公開後確認と未実施チェックの整理を行う | task_worker | pending | `README.md`, `docs/HUMAN_MANUAL.md`, `docs/exec-plans/active/attention-queue.md` | TICKET-2026-03-10-031 |

## 完了条件
- 公開 URL を参照できる
- 初回 publish の結果と、まだ未実施の link check / 追加 lint が区別されている

## Done チェック
- [ ] 含まれる ticket がすべて `done`
- [ ] chunk review の重大 findings が解消済み
- [ ] docs / status 更新が完了している
- [ ] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に publish し、その後で公開後確認と残課題整理を行う

## chunk review 観点
- 「公開できたこと」と「まだやっていない品質確認」が混同されていないか
- 初回 publish の記録が後から追えるか
