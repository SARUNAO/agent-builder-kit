---
chunk_id: CHUNK-2026-03-10-011
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-003
title: 「真のハーネスエンジニアリングへ至るには？」章を書く
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-010
lane_order: 1100
kind: chunk
---

# 「真のハーネスエンジニアリングへ至るには？」章を書く

- chunk_id: CHUNK-2026-03-10-011
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-003
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-010
- lane_order: 1100

## chunk の目的
- 現在の `agent-builder-kit` の到達点と限界を整理し、より強いハーネスエンジニアリングへ拡張する方向性を章として説明する
- マルチエージェント化、並列実行、CI/CD、境界の視覚化、専用 Skill 拡張などの将来案を読者へ示す

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-021 | `真のハーネスエンジニアリングへ至るには？` 章の本文ドラフトを作る | task_worker | done | `src/true-harness-engineering.md`, `src/SUMMARY.md` | TICKET-2026-03-10-020 |
| TICKET-2026-03-10-022 | `真のハーネスエンジニアリングへ至るには？` 章の推敲と根拠同期を行う | task_worker | done | `src/true-harness-engineering.md`, `src/SUMMARY.md`, `docs/exec-plans/active/article-source-map.md` | TICKET-2026-03-10-021 |

## 完了条件
- 現状の kit でできていることと、まだ足りないことが章単体で整理されている
- 並列化、CI/CD、レイヤードアーキテクチャ、専用 Skill 拡張といった将来案が、夢物語ではなく導入候補として説明されている

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に現状課題と拡張案の本文ドラフトを作り、そのあとで推敲と根拠同期を行う

## chunk review 観点
- 現状批判だけで終わらず、拡張可能性が具体的に見えるか
- 並列化やマルチエージェント化の話が、現在の docs 駆動フローと接続しているか
- `agent-builder-kit` の拡張案が抽象論ではなく、Skill や構造の追加候補として読めるか
