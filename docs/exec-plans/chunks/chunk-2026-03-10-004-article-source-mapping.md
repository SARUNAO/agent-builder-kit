---
chunk_id: CHUNK-2026-03-10-004
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-007
title: 実例ログを記事素材へ変換する
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-003
lane_order: 400
kind: chunk
---

# 実例ログを記事素材へ変換する

- chunk_id: CHUNK-2026-03-10-004
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-007
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-003
- lane_order: 400

## chunk の目的
- BLK-002 の作業結果から、記事化に使える一次記録を回収する
- 後続の BLK-003 が、どの記録をどの章の根拠に使うか見えるようにする

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-007 | BLK-002 の実例を decision / gotcha / command / before-after に落とす | task_worker | done | `docs/exec-plans/active/*.md`, `docs/exec-plans/fact-reports/*.md` | TICKET-2026-03-10-006 |
| TICKET-2026-03-10-008 | 記録から記事素材マップを作る | task_worker | done | `docs/exec-plans/active/*.md`, `src/**/*.md` | TICKET-2026-03-10-007 |

## 完了条件
- BLK-002 の主要な判断、コマンド、詰まり、差分が一次記録へ落ちている
- BLK-003 が章ごとの根拠を辿れる記事素材マップが存在する

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- まず一次記録を埋めてから、章との対応表を作る

## 統合時の注意
- 事実と解釈を混ぜない
- mdBook 本文へ直接書き込みすぎず、BLK-003 の余地を残す

## chunk review 観点
- 記録が BLK-002 の実態と矛盾していないか
- 記事素材マップが BLK-003 の起点として十分か

## 進捗メモ
- 2026-03-10: BLK-007 の後半として、実例ログ回収と章素材マッピングを切り出した
- 2026-03-10: TICKET-007 を `done` に昇格し、BLK-002 の一次記録を 4 系統の active logs へ retro 収集した
- 2026-03-10: root `asset/` に補助スナップショットが追加されたため、TICKET-008 で記事素材マップへ取り込む
- 2026-03-10: TICKET-008 を `done` に昇格し、4 章分の記事素材マップと補助アセット対応を整理した
