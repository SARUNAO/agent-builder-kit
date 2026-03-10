---
ticket_id: TICKET-2026-03-10-004
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-002
title: build / serve の確認手順を残す
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - README.md
  - src/
lane_order: 200
depends_on: TICKET-2026-03-10-003
kind: ticket
---

# build / serve の確認手順を残す

- ticket_id: TICKET-2026-03-10-004
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-002
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- ローカルで `mdbook build` と `mdbook serve --open` をどう確認するかを repo 内に残す

## やること
- `mdbook build` を実行し、結果を確認する
- 可能なら `mdbook serve --open` の試行条件を確認する
- `README.md` に build / serve の確認手順と、失敗時の見方を追記する

## やらないこと
- GitHub Pages への deploy
- link check の導入
- ワークショップ本文の詳細化

## Editable Paths
- `README.md`
- `src/`

## Inputs
- TICKET-2026-03-10-001 で整理した導入手順
- TICKET-2026-03-10-003 で配置した `src/`

## Implementation Notes
- `mdbook serve --open` が GUI 制約で難しい場合は、`mdbook serve` までで止めてもよい
- コマンドが失敗したら、失敗内容を `fact-report` に残す
- 必要なら README の文面は「初めての人向け」に寄せる

## Verification
- `mdbook build` の成功、または失敗理由の記録がある
- `README.md` にローカル確認手順が残っている

## Done When
- ローカル確認の最小手順が repo 内に残っている
- BLK-003 へ進む前の足場が揃っている

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] reviewer からの承認、または重大 findings 解消済みを確認した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 手順と実際の repo 状態が矛盾していないか

## 完了時に返すもの
- `fact-report`
- 実行コマンド
- build / serve の結果
- 未解決事項
- command / gotcha 候補のメモ

## 実施結果
- `mdbook build` を実行し、`book/` に HTML が生成されることを確認した
- `mdbook serve --open` は sandbox 内では bind 制約で失敗しうるため、その事実を記録した
- 制限外では `mdbook serve --open --hostname 127.0.0.1 --port 3001` で watcher 起動まで確認した
- `README.md` に build / serve の最小手順と、sandbox 制約時の見方を追加した
- この ticket は markdown / docs 更新主体なので reviewer は docs-only skip とする

## Verification 結果
- `mdbook build` が成功した
- `README.md` にローカル確認手順を追記した
- `mdbook serve --open` は通常ローカルでは起動できる一方、sandbox では `Operation not permitted (os error 1)` が出ることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-004-local-verification.md`
