---
chunk_id: CHUNK-2026-03-10-002
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-002
title: 初期章の配置とローカル検証を揃える
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-001
lane_order: 200
kind: chunk
---

# 初期章の配置とローカル検証を揃える

- chunk_id: CHUNK-2026-03-10-002
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-002
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-001
- lane_order: 200

## chunk の目的
- `BLK-003` へ渡すための最小章構成を仮置きする
- `mdbook build` と、可能なら `mdbook serve --open` の確認手順を固める

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-003 | 初期の章ファイルと `SUMMARY.md` を整える | task_worker | done | `src/SUMMARY.md`, `src/**/*.md` | TICKET-2026-03-10-002 |
| TICKET-2026-03-10-004 | build / serve の確認手順を残す | task_worker | done | `README.md`, `src/**` | TICKET-2026-03-10-003 |

## 完了条件
- 4 章前後の最小構成が `src/` に配置されている
- `mdbook build` の確認結果が残っている
- `mdbook serve --open` を試せる条件と、試せない場合の扱いが docs に明記されている
- BLK-007 が拾える一次記録の素材が fact-report と返却物に残っている

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 並列化ルール
- この chunk の ticket は直列実行とする
- `SUMMARY.md` と章ファイルが先に固まらないと build / serve の検証ができない

## 統合時の注意
- 章タイトルは BLK-003 で増やせるよう、過剰に本文を書き込まない
- `mdbook serve --open` が実行できない環境では、理由を fact-report と ticket に残す

## chunk review 観点
- 初期章の配置が BLK-003 の本文作成を邪魔しないか
- build / serve の確認手順が README と fact-report で矛盾しないか
- 後続の記録 block が再利用できる事実が残っているか

## 進捗メモ
- 2026-03-10: 骨格生成の後段として、章配置とローカル検証を別 chunk に切り出した
- 2026-03-10: TICKET-003 で初期 4 章の最小スタブと `SUMMARY.md` の対応を整えた
- 2026-03-10: TICKET-004 を `done` に昇格し、build / serve の確認結果を README と fact-report へ反映した
