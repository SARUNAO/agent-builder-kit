---
chunk_id: CHUNK-2026-03-10-014
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_block: BLK-004
title: GitHub Pages 公開の骨格を作る
status: done
owner_role: task_planner
depends_on: CHUNK-2026-03-10-013
lane_order: 1400
kind: chunk
---

# GitHub Pages 公開の骨格を作る

- chunk_id: CHUNK-2026-03-10-014
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_block: BLK-004
- status: done
- owner_role: task_planner
- depends_on: CHUNK-2026-03-10-013
- lane_order: 1400

## chunk の目的
- GitHub Pages と GitHub Actions で公開するための最小骨格を作る
- `book.toml` と workflow に、初回 publish に必要な最小設定を入れる

## 含む ticket
| ticket_id | title | owner | status | editable_paths | depends_on |
|---|---|---|---|---|---|
| TICKET-2026-03-10-027 | GitHub Pages 公開向けに `book.toml` と workflow 骨格を追加する | task_worker | done | `book.toml`, `.github/workflows/mdbook-pages.yml` | TICKET-2026-03-10-026 |
| TICKET-2026-03-10-028 | Pages 公開骨格の推敲と前提整理を行う | task_worker | done | `book.toml`, `.github/workflows/mdbook-pages.yml`, `docs/exec-plans/active/attention-queue.md` | TICKET-2026-03-10-027 |

## 完了条件
- GitHub Pages で mdBook を deploy する workflow 骨格が入っている
- `book.toml` に公開前提の最小設定方針が入っている
- URL 未確定部分は placeholder や TODO として明示されている

## Done チェック
- [x] 含まれる ticket がすべて `done`
- [x] chunk review の重大 findings が解消済み
- [x] docs / status 更新が完了している
- [x] `plan-owner` に done 昇格判断を渡せる状態になっている

## 進捗メモ
- 2026-03-10: GitHub Pages workflow 骨格、`book.toml` の公開設定、post-publish の TODO 整理まで完了した

## 並列化ルール
- この chunk の ticket は直列実行とする
- 先に deploy 骨格を作り、そのあとで前提や TODO を整理する

## chunk review 観点
- URL 未確定のままでも進められる最小骨格に留まっているか
- GitHub Pages と Actions の責務が混ざりすぎていないか
