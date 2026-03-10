---
chunk_id: CHUNK-2026-03-10-005
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 導入章と主題の置き方を固める
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-004
lane_order: 500
kind: chunk
---

# 導入章と主題の置き方を固める

- chunk_id: CHUNK-2026-03-10-005
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-004
- lane_order: 500

## chunk の目的
- 「まえがき」または「はじめに」に相当する導入章を置き、この mdBook 全体の骨子を最初に説明できるようにする
- 既存 4 章の導入文を、mdBook 主体ではなく `agent-builder-kit` 主体へ寄せる

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-009 | 「はじめに」章を追加し、この mdBook の骨子を最初に説明する | task_worker | done | `src/SUMMARY.md`, `src/introduction.md`, `src/overview.md` | TICKET-2026-03-10-008 |
| TICKET-2026-03-10-010 | 既存 4 章の導入文を `agent-builder-kit` 主軸へ寄せる | task_worker | done | `src/overview.md`, `src/plan-manager-skeleton.md`, `src/role-flow.md`, `src/first-change.md` | TICKET-2026-03-10-009 |

## 完了条件
- 読み始めてすぐ、この mdBook が mdBook 入門ではなく `agent-builder-kit` tutorial を主軸にしていると分かる
- 既存 4 章が、新しい主題配分 3:7 と矛盾しない

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に「はじめに」章で全体の骨子を置いてから、既存章の導入文を調整する

## 統合時の注意
- タイトルページ custom はこの段階では優先しない
- 歓迎文を入れても、根拠と一次記録への導線は残す

## chunk review 観点
- 導入章が `agent-builder-kit` tutorial であることを明確にできているか
- 既存 4 章との役割分担が崩れていないか

## 進捗メモ
- 2026-03-10: BLK-003 の最初の着手点として、「はじめに」章と主題の置き方を先に固める chunk を追加した
- 2026-03-10: TICKET-009 と TICKET-010 が完了し、章別 chunk へ分けて本文へ入る前段整理は完了した
