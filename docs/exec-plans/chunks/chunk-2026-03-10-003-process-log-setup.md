---
chunk_id: CHUNK-2026-03-10-003
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-007
title: 一次記録の置き場と運用ルールを整える
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-002
lane_order: 300
kind: chunk
---

# 一次記録の置き場と運用ルールを整える

- chunk_id: CHUNK-2026-03-10-003
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-007
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-002
- lane_order: 300

## chunk の目的
- decision / gotcha / command / before-after をどこへ残すか決める
- 以後の ticket が同じ粒度で記録を返せるルールを整える

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-005 | 一次記録 docs の置き場と index を作る | task_worker | done | `docs/exec-plans/active/index.md`, `docs/exec-plans/active/*.md` | TICKET-2026-03-10-004 |
| TICKET-2026-03-10-006 | `fact-report` と記録ルールを揃える | task_worker | done | `docs/templates/fact-report-template.md`, `README.md`, `docs/HUMAN_MANUAL.md` | TICKET-2026-03-10-005 |

## 完了条件
- 一次記録の置き場が repo 内で明示されている
- `fact-report` と補助 docs が、後続 ticket に同じ記録粒度を要求できる
- BLK-002 の完了物を BLK-007 が回収できる状態になっている

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に置き場を作ってから、`fact-report` と guidance を寄せる

## 統合時の注意
- raw な内部メモを公開前提 docs に混ぜすぎない
- 初学者が「何をどこへ記録するか」を迷わない粒度に留める

## chunk review 観点
- 置き場とルールが過剰に複雑でないか
- BLK-002 / BLK-003 の worker がそのまま運用できるか

## 進捗メモ
- 2026-03-10: BLK-007 の前半として、記録ストアと運用ルール整備を切り出した
- 2026-03-10: TICKET-005 着手に合わせて、この chunk を `in_progress` に上げた
- 2026-03-10: TICKET-005 を `done` に昇格し、`docs/exec-plans/active/` に一次記録のホームを作成した
- 2026-03-10: TICKET-006 を `done` に昇格し、`fact-report` template と記録ルールを README / Human Manual に反映した
