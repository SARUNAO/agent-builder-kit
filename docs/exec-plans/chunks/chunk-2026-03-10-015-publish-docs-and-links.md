---
chunk_id: CHUNK-2026-03-10-015
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-004
title: 公開導線を README と本文へ反映する
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-014
lane_order: 1500
kind: chunk
---

# 公開導線を README と本文へ反映する

- chunk_id: CHUNK-2026-03-10-015
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-004
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-014
- lane_order: 1500

## chunk の目的
- GitHub 上の公開導線を README と本文へ反映する
- 同一 repo で `agent-builder-kit` と mdBook をどう参照するかを読者向けに整理する

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-029 | README と補助 docs に GitHub 公開導線を追加する | task_worker | done | `README.md`, `docs/HUMAN_MANUAL.md` | TICKET-2026-03-10-028 |
| TICKET-2026-03-10-030 | 本文と公開導線の表現を同期する | task_worker | done | `src/overview.md`, `src/conclusion.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-029 |

## 完了条件
- README と補助 docs から公開 site と repo 構造が追える
- 本文にも同一 repo 前提の公開導線が自然に反映されている

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 進捗メモ
- 2026-03-10: README / Human Manual / 本文 / source map に公開導線を反映し、同一 repo 前提の読者導線を閉じた

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に README / manual の導線を固め、その後で本文の表現を合わせる

## chunk review 観点
- repo 説明と公開 site 説明が矛盾していないか
- `agent-builder-kit` と mdBook の関係が同一 repo 前提で分かるか
