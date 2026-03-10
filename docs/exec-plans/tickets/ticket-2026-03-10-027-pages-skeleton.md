---
ticket_id: TICKET-2026-03-10-027
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-014
title: GitHub Pages 公開向けに `book.toml` と workflow 骨格を追加する
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - book.toml
  - .github/workflows/mdbook-pages.yml
lane_order: 100
depends_on: TICKET-2026-03-10-026
kind: ticket
---

# GitHub Pages 公開向けに `book.toml` と workflow 骨格を追加する

- ticket_id: TICKET-2026-03-10-027
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-014
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- GitHub Pages で mdBook を deploy するための最小骨格を追加する

## やること
- `book.toml` に公開前提の最小設定を追加する
- GitHub Actions で build / deploy する workflow 骨格を追加する
- URL 未確定部分は TODO や placeholder として残す

## Editable Paths
- `book.toml`
- `.github/workflows/mdbook-pages.yml`

## Verification
- workflow と `book.toml` の構成が、GitHub Pages publish の骨格として読める

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `book.toml` に GitHub Pages 公開前提の最小設定を追加した
- `.github/workflows/mdbook-pages.yml` を新規作成し、build / upload / deploy の最小 workflow 骨格を追加した
- 公開 URL 未確定部分は `REPO_NAME` / `OWNER` の placeholder と TODO コメントで残した
- workflow と deploy 設定の変更があるため、docs-only skip にはせず reviewer handoff 前提とする

## Verification 結果
- `mdbook build` を実行し、`book.toml` 更新後も book が生成できることを確認した
- workflow 構成が `checkout -> configure-pages -> mdbook build -> upload artifact -> deploy` になっていることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-027-pages-skeleton.md`

## Reviewer Findings
- `book.toml` の `site-url` と `git-repository-url` が placeholder のままなので、この状態で Pages へ出すと公開 URL や repository link が壊れる。初回 publish 前に実 repo 名へ差し替えるか、未確定なら workflow と同時に上書きする仕組みが必要。

## Planner 裁定メモ
- 上記 finding は `TICKET-2026-03-10-028` で workflow 側の placeholder 解決を追加し、解消済みと判断する
