---
reference_id: REF-ATTENTION
title: Attention Queue
lane_order: 300
owner_role: task_planner
sync_mode: direct_source
kind: reference_source
---

# ATTENTION Queue

「今は実装しないが、後で必ず再注目する事項」を管理する台帳。

## ルール
- 新規の後回し事項は、このファイルへ 1 行追加する。
- 実装開始時に `trigger` と現在タスクを照合し、該当すれば宣言する。
- 完了時は `status` を `done` にし、`closed_on` を埋める。

## Active Items
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-SEED-001 | pending | bootstrap 直後に package tree を点検するとき | compiled artefact cluster (`__pycache__` など再生成可能な生成物) が残っていれば削除する | `docs/HUMAN_MANUAL.md`, `docs/OPERATIONAL_SCHEMA.md` | bootstrap | - | AI案内可 / `safe-delete` |
| ATN-SEED-002 | pending | reference band や direct-source 運用を確認するとき | band 用 summary / hub note cluster は direct-source と link 検証が揃った場合だけ縮退・未生成許容を見直す | `docs/HUMAN_MANUAL.md`, `docs/OPERATIONAL_SCHEMA.md` | bootstrap | - | 条件付き / `requires-contract-change` |
| ATN-SEED-003 | pending | package cleanup 方針を決めるとき | 補助 reference docs と stale instruction cluster の keep / archive / cleanup は人間が裁定する | `docs/HUMAN_MANUAL.md`, `docs/ROLE_SKILLS.md` | bootstrap | - | 人間判断必須 / `requires-human-approval`, `requires-package-decision` |

## Template
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-YYYY-MM-DD-XXX | pending | どの作業に入ったら再注目するか | 必須実装 / 必須確認事項 | 関連 docs へのリンク | YYYY-MM-DD | - | 補足 |

## reference summary との分担
- この file は reference band の本体 docs として扱う
- `docs/references/attention-queue.md` は optional summary / hub として残してよい
- summary を残す場合も、canvas band の代替正本にはしない
- 本体には active item と trigger を残し、summary には短い見取り図だけを置く

## static seed 契約
- package / generated の static queue seed 正本は、この file の `Active Items` に置く
- `init_runner.py` は code string を別管理せず、この file を読んで generated `attention-queue.md` を初期化する
- static item の文言は file 名列挙ではなく cleanup cluster 名ベースに留める
