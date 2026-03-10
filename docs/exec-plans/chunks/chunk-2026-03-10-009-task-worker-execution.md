---
chunk_id: CHUNK-2026-03-10-009
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 「task-worker で ticket を実行し、fact-report を返す」章を書く
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-008
lane_order: 900
kind: chunk
---

# 「task-worker で ticket を実行し、fact-report を返す」章を書く

- chunk_id: CHUNK-2026-03-10-009
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-008
- lane_order: 900

## chunk の目的
- `first-change.md` を、`task-worker` が ticket を実行し、fact-report を返す章へ育てる
- 実装、事実報告、必要なら reviewer handoff までをひとつの流れとして見せる

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-017 | `task-worker で ticket を実行し、fact-report を返す` 章の本文ドラフトを作る | task_worker | done | `src/first-change.md`, `src/SUMMARY.md` | TICKET-2026-03-10-016 |
| TICKET-2026-03-10-018 | `task-worker で ticket を実行し、fact-report を返す` 章の推敲と根拠同期を行う | task_worker | done | `src/first-change.md`, `src/SUMMARY.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-017 |

## 完了条件
- `task-worker` が何を実装し、何を返す role かを章単体で追える
- `fact-report` と reviewer handoff の位置づけが章内で混線していない

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に本文ドラフトを作り、そのあとで推敲と根拠同期を行う

## chunk review 観点
- `task-worker` の責務と reviewer handoff の位置づけが自然に読めるか
- `fact-report` を返す意味が本文で分かるか
- 章タイトルが本文の内容とずれる場合は、タイトル変更も許容する
