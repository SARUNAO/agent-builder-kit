---
ticket_id: TICKET-2026-03-10-011
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-006
title: `agent-builder-kit の導入` 章の本文ドラフトを作る
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/overview.md
lane_order: 100
depends_on: TICKET-2026-03-10-010
kind: ticket
---

# `agent-builder-kit の導入` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-011
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-006
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 100
- last_updated: 2026-03-10

## Goal
- `overview.md` を、`agent-builder-kit` の思想とこの project での使い方が伝わる導入章ドラフトへ育てる

## やること
- `AGENTS.md`, `docs/`, role 分担をどう使うかの説明を短く加える
- mdBook を題材に選んだ理由を、成果物例としての位置づけで整理する
- 後続の「環境確認」章へつながる終わり方にする
- 本文の流れに合わせて必要なら章タイトル変更案も出す

## やらないこと
- 全 role の詳細仕様をここで書き切ること
- `AGENTS.md` や docs schema の全文解説

## Editable Paths
- `src/overview.md`

## Inputs
- `src/introduction.md`
- `docs/exec-plans/active/article-source-map.md`
- `AGENTS.md`

## Verification
- 章単体で読んでも `agent-builder-kit` の導入になっている
- mdBook が主役ではなく成果物例として位置づいている

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## 実施結果
- `overview.md` の既存導入文は削除し、新規プロジェクトで `agent-builder-kit` を初期化する最初の手順へ差し替えた
- 公開 repo への導線を置く前提で、公開前の注意書きを本文先頭に追加した
- 章の入口として、最初の節見出しを `新規プロジェクトを開始` に整理した
- Codex アプリで新規プロジェクトを開き、空のルートディレクトリへ `.obsidian`, `agent-builder-kit`, `docs-builder.toml` を置く流れをコードブロック付きで記述した
- 各項目について、役割と最初にやることを短く説明した
- 各項目説明の書式は、見出しではなくフラットな箇条書きへ整えた
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- 章単体で読んでも、最初に何を配置するかが分かる構成になった
- 既存の抽象説明を外し、初期化手順の導入として読める章になった
- 公開前であることと、後で GitHub リンクへ差し替える前提が本文から分かる
- `mdbook build` が成功し、章の差し替え後も book が生成できることを確認した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-011-agent-builder-kit-intro-draft.md`
