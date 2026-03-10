---
chunk_id: CHUNK-2026-03-10-007
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 「plan-manager でプロジェクトの骨子を組む」章を書く
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-006
lane_order: 700
kind: chunk
---

# 「plan-manager でプロジェクトの骨子を組む」章を書く

- chunk_id: CHUNK-2026-03-10-007
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-006
- lane_order: 700

## chunk の目的
- `overview.md` の初期化導線を受けて、次に `plan-manager` で何を決めるのかを章として説明する
- project-intake, discovery-brief, plan-spec, block note がどう生まれるかを追える本文へ育てる

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-013 | `plan-manager でプロジェクトの骨子を組む` 章の本文ドラフトを作る | task_worker | done | `src/plan-manager-skeleton.md`, `src/SUMMARY.md` | TICKET-2026-03-10-012 |
| TICKET-2026-03-10-014 | `plan-manager でプロジェクトの骨子を組む` 章の推敲と根拠同期を行う | task_worker | done | `src/plan-manager-skeleton.md`, `src/SUMMARY.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-013 |

## 完了条件
- `plan-manager` が project の骨子をどう組み立てるかを章単体で追える
- `project-intake`, `discovery-brief`, `plan-spec`, block note の役割が章内で混線していない

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に本文ドラフトを作り、そのあとで推敲と根拠同期を行う

## chunk review 観点
- `plan-manager` の役割が chunk / ticket の役割と混線していないか
- 章が「骨子づくり」の話として自然に読めるか
- 本文に合わせて章タイトルを調整したほうが自然なら、タイトル変更も許容する
