---
ticket_id: TICKET-2026-03-10-002
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-001
title: `mdbook init` で最小骨格を作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - book.toml
  - src/
lane_order: 200
depends_on: TICKET-2026-03-10-001
kind: ticket
---

# `mdbook init` で最小骨格を作る

- ticket_id: TICKET-2026-03-10-002
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-001
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- 公式に沿った最小 mdBook 骨格を repo に作り、後続で章追加できる状態にする

## やること
- `mdbook init` で `book.toml` と `src/` を生成する
- 生成物を確認し、不要なサンプル本文があれば最小限に整える
- `BLK-003` で使う前提として `SUMMARY.md` と初期章ファイルが触れる状態にしておく

## やらないこと
- 章本文の本格執筆
- build / serve の最終確認
- GitHub Pages 用の publish 設定

## Editable Paths
- `book.toml`
- `src/`

## Inputs
- `docs/exec-plans/blocks/block-002-mdbook-skeleton.md`
- `README.md`
- TICKET-2026-03-10-001 の導入手順

## Implementation Notes
- `mdbook init` が使えない場合は、そこで止めず blocked 理由を ticket と fact-report に残す
- 生成物は後続 ticket が diff を追いやすいよう、最小限の整理に留める

## Verification
- `book.toml` と `src/SUMMARY.md` が存在する
- 章追加の前提になる最小構造が揃っている

## Done When
- repo 内に mdBook の最小骨格が存在する
- 後続 ticket が章配置に着手できる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] reviewer からの承認、または重大 findings 解消済みを確認した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 生成物の整理が後続の章作成を妨げないか

## 完了時に返すもの
- `fact-report`
- 実行コマンド
- 生成された主要ファイルの一覧
- 未解決事項
- before / after と decision 候補のメモ

## 実施結果
- `cargo install mdbook` で `mdbook v0.5.2` を導入した
- `mdbook init --force --title "mdBook Workshop" .` を実行して `book.toml` と `src/` を生成した
- 生成直後の `chapter_1.md` は `overview.md` へ寄せ、`SUMMARY.md` とあわせて日本語の最小スタブへ整えた
- `book.toml` と `src/` の実ファイルを更新しているため、reviewer handoff 対象とする

## Verification 結果
- `mdbook --version` が `mdbook v0.5.2` を返すことを確認した
- `book.toml` と `src/SUMMARY.md` が生成されていることを確認した
- `src/overview.md` が存在し、`src/SUMMARY.md` から参照されていることを確認した
- reviewer 観点で `mdbook build` を追加実行し、HTML 出力まで成功することを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-002-mdbook-init.md`

## Review 結果
- reviewer: no findings
- 確認観点: 生成物の命名、最小骨格の整合、後続 ticket への受け渡し、`mdbook build` の成立
