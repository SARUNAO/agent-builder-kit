---
chunk_id: CHUNK-2026-03-10-008
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 「task-planner で仕事を chunk と ticket に分ける」章を書く
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-007
lane_order: 800
kind: chunk
---

# 「task-planner で仕事を chunk と ticket に分ける」章を書く

- chunk_id: CHUNK-2026-03-10-008
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-007
- lane_order: 800

## chunk の目的
- `role-flow.md` を、`task-planner` が work を chunk と ticket へ分ける章へ育てる
- plan-spec と block から、実行可能な単位へどう分解するかを文章化する

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-015 | `task-planner で仕事を chunk と ticket に分ける` 章の本文ドラフトを作る | task_worker | done | `src/role-flow.md`, `src/SUMMARY.md` | TICKET-2026-03-10-014 |
| TICKET-2026-03-10-016 | `task-planner で仕事を chunk と ticket に分ける` 章の推敲と根拠同期を行う | task_worker | done | `src/role-flow.md`, `src/SUMMARY.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-015 |

## 完了条件
- `task-planner` が block を chunk / ticket へどう分解するかを章単体で追える
- 分解粒度と handoff の考え方が章内で混線していない

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に本文ドラフトを作り、そのあとで推敲と根拠同期を行う

## chunk review 観点
- `task-planner` の役割が `plan-manager` や `task-worker` と混線していないか
- chunk / ticket の分け方が本文で自然に説明されているか
- 本文の重心に応じて章タイトルを変えたほうがよい場合は、その変更も許容する
