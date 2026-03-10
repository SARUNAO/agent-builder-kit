---
chunk_id: CHUNK-2026-03-10-010
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 「開発ログからチュートリアル本文を組み立てる」章を書く
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-009
lane_order: 1000
kind: chunk
---

# 「開発ログからチュートリアル本文を組み立てる」章を書く

- chunk_id: CHUNK-2026-03-10-010
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-009
- lane_order: 1000

## chunk の目的
- 開発中に残した planning docs と active logs を、どうチュートリアル本文へ再構成するかを章として説明する
- この project 自体を教材化する流れを、読者が再利用できる形で見せる

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-019 | `開発ログからチュートリアル本文を組み立てる` 章の本文ドラフトを作る | task_worker | done | `src/process-to-article.md`, `src/SUMMARY.md` | TICKET-2026-03-10-018 |
| TICKET-2026-03-10-020 | `開発ログからチュートリアル本文を組み立てる` 章の推敲と根拠同期を行う | task_worker | done | `src/process-to-article.md`, `src/SUMMARY.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-019 |

## 完了条件
- 計画 docs、fact-report、active logs をどう本文へ変換するかが章単体で追える
- この repo の開発フローを、他の成果物へ転用できる視点が伝わる

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に本文ドラフトを作り、そのあとで推敲と根拠同期を行う

## chunk review 観点
- 記録を本文へ変換する価値が具体的に伝わるか
- この project 固有の話と、他へ転用できる話が混線していないか
