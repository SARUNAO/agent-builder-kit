---
ticket_id: TICKET-2026-03-10-028
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-014
title: Pages 公開骨格の推敲と前提整理を行う
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - book.toml
  - .github/workflows/mdbook-pages.yml
  - docs/exec-plans/active/attention-queue.md
lane_order: 200
depends_on: TICKET-2026-03-10-027
kind: ticket
---

# Pages 公開骨格の推敲と前提整理を行う

- ticket_id: TICKET-2026-03-10-028
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-014
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- GitHub Pages publish の骨格に残る前提や TODO を整理する

## やること
- workflow と `book.toml` の表現を推敲する
- attention queue に残すべき公開前提や post-publish 項目を整理する
- 初回 publish の最小ゲートが `mdbook build` であることを docs と整合させる

## Editable Paths
- `book.toml`
- `.github/workflows/mdbook-pages.yml`
- `docs/exec-plans/active/attention-queue.md`

## Verification
- 初回 publish と post-publish 改善項目の境界が docs 上で分かる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- reviewer 指摘を受けて、workflow 側で `book.toml` の placeholder を repository 情報から置換する手順を追加した
- `book.toml` の placeholder は未確定値ではなく、CI で解決する前提の marker であると明記した
- `attention-queue` に、publish 後に実公開 URL を README / 本文へ反映する項目を追加した
- workflow と deploy 設定の変更が続くため、docs-only skip にはせず reviewer handoff 前提を維持する

## Verification 結果
- `mdbook build` を実行し、`book.toml` 更新後も book が生成できることを確認した
- workflow が `Resolve Pages URLs -> mdbook build` の順で実行されることを確認した
- 初回 publish と post-publish docs 反映の境界が `attention-queue` で分かれることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-028-pages-skeleton-polish.md`

## Reviewer Sign-off
- findings なし
- 確認観点: placeholder 解消、workflow の build / deploy 導線、publish 前後の責務分離
- 残留リスク: user / org Pages ではなく project Pages 前提の path 解決なので、その前提を外す場合は `site-url` 解決方針を再調整する
