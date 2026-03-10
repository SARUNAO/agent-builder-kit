---
ticket_id: TICKET-2026-03-10-009
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-005
title: 「はじめに」章を追加し、この mdBook の骨子を最初に説明する
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/SUMMARY.md
  - src/introduction.md
  - src/overview.md
lane_order: 100
depends_on: TICKET-2026-03-10-008
kind: ticket
---

# 「はじめに」章を追加し、この mdBook の骨子を最初に説明する

- ticket_id: TICKET-2026-03-10-009
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-005
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- 読み始めた時点で、この mdBook の主題が `agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングにあると分かる導入を作る

## やること
- `src/SUMMARY.md` の先頭に「はじめに」章を追加する
- `src/introduction.md` を新規作成し、この mdBook の骨子と読む順番を短く説明する
- 既存の `overview.md` と役割が重なる場合は、導入と本論の境界が分かるよう最小限に整理する

## やらないこと
- タイトルページ custom の導入
- 全章の本文をこの ticket で書き切ること
- mdBook の一般入門を主役に戻すこと

## Editable Paths
- `src/SUMMARY.md`
- `src/introduction.md`
- `src/overview.md`

## Inputs
- `docs/exec-plans/blocks/block-003-workshop-content.md`
- `docs/exec-plans/active/article-source-map.md`
- `asset/初回plan-manager実行後に生成された開発フロー.png`

## Implementation Notes
- 第一候補は title page custom ではなく、「はじめに」章の追加
- 文体は planning docs より少しやわらかくしてよい
- ただし歓迎文のあとに、この mdBook が何を扱い、何を扱わないかを明示する

## Verification
- `SUMMARY.md` の先頭から「はじめに」章へ辿れる
- 「mdBook 入門が主役ではない」ことが導入だけで分かる

## Done When
- BLK-003 の入口として機能する導入章が repo に入っている

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 導入章が `agent-builder-kit` tutorial の入口として十分か

## 完了時に返すもの
- `fact-report`
- 追加した導入文
- 既存 `overview.md` との役割分担メモ

## 実施結果
- `src/SUMMARY.md` の先頭に「はじめに」章を追加した
- `src/introduction.md` を新規作成し、この mdBook の主題が `agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングにあることを先に明示した
- `src/overview.md` は本論側の入口へ寄せ、導入章との役割重複を減らした
- 人間レビューでの文面推敲を反映し、「扱うこと / 扱わないこと」と参考記事リンクを追加した
- 「はじめに」章の中では目次を持たせず、章内案内にあたる段落を削除した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- `src/SUMMARY.md` の先頭から「はじめに」章へ辿れることを確認した
- `mdbook build` が成功し、追加した章を含めて book が生成できることを確認した
- 導入文だけで「mdBook 入門が主役ではない」ことが読み取れる構成にした

## 役割分担メモ
- `introduction.md`: この mdBook が何を扱い、何を主役にしないかを先に伝える入口
- `overview.md`: 上の方針を受けて、この project の成果物と進め方を本論側へつなぐ章

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-009-introduction-chapter.md`
