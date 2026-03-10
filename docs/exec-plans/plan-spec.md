# Plan Spec

- plan_id: PLAN-2026-03-10-MDBOOK-WORKSHOP
- status: in_progress
- owner: プランオーナー
- priority: high
- last_updated: 2026-03-10
- source_intake: INTAKE-2026-03-10
- source_discovery: DISCOVERY-2026-03-10

## 目的
- agent-builder の実運用を題材に、mdBook でワークショップ記事サイトを構築するプロジェクト

## High-level blocks
| block_id | title | goal | status | depends_on |
|---|---|---|---|---|
| BLK-001 | 初期スコープと公開方針を固める | 現状事実、公開ゴール、推奨方針を整理し、後続 block の前提を確定する | done | - |
| BLK-002 | mdBook の最小骨格を作る | `book.toml` と `src/` の最小構成を作り、ローカル build 可能な状態にする | pending | BLK-001 |
| BLK-003 | ワークショップ章を作る | agent-builder の流れを体験できる章構成と本文を作成する | pending | BLK-002 |
| BLK-004 | GitHub 公開と配布導線を作る | GitHub 上で mdBook と関連成果物を公開し、チュートリアルとして参照できる状態にする | pending | BLK-003 |
| BLK-005 | 運用導線と仕上げを整える | README、Human Manual、必要な補助 docs を更新し、再開しやすいワークショップ状態にする | pending | BLK-004 |
