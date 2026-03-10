# Adoption Plan

- adoption_plan_id: ADOPT-2026-03-09
- related_plan: PLAN-2026-03-09-DOCS-BUILDER
- status: ready
- owner: プランオーナー
- last_updated: 2026-03-09

## 目的
- 既存運用を保ったまま、この repo 自身が docs_builder の生成物でも再現できることを確認する。
- そのうえで、`migration-bootstrap/` の内容をこの repo の正式運用へ段階的に採用する。

## フェーズ
| phase | goal | scope | exit_criteria | owner |
|---|---|---|---|---|
| 1 | 現行正本の保全 | `AGENTS.md`, `docs/`, root artefact の backup | rollback 用の退避先が作られている | plan-owner |
| 2 | core docs の正式採用 | `AGENTS.md`, `README.md`, `docs/` core, `docs/references/`, `docs/exec-plans/` | self-hosting で一致した範囲が root へ反映される | plan-owner |
| 3 | additive docs の正式採用 | `docs/migration/`, `docs/templates/` | migration / template docs が root 配下へ追加される | plan-owner |
| 4 | root planning/runtime の昇格 | `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`, `docs/exec-plans/canvas/`, `docs/references/` | planning runtime artefact が正式運用へ入る | task-planner |
| 5 | migration の後処理方針確定 | `MIGRATION_START_HERE.md`, `docs/migration/` の残置/整理 | 移行完了後の扱いが明文化される | plan-owner |

## 採用方針
- `AGENTS.md` と `docs/` の自己記述 docs は、`self_hosting_pack` の source 継承結果を正式採用する
- `docs/migration/` は当面残し、移行判断と履歴の作業台として使う
- `docs/templates/` は builder 自身の正本にも含めてよい
- `docs-builder.toml` はこの repo の恒久 root artefact として置く
- `MIGRATION_START_HERE.md` は migration 期間中は root に置き、移行完了後の残置は別途判断する

## 実行順
1. 現行 `AGENTS.md`, `docs/`, root artefact を `backup/` か同等の退避先へ保全する
2. `migration-bootstrap/AGENTS.md`, `migration-bootstrap/README.md`, `migration-bootstrap/docs/` のうち一致確認済み範囲を root へ反映する
3. `migration-bootstrap/docs/migration/` と `migration-bootstrap/docs/templates/` を root `docs/` 配下へ追加する
4. `migration-bootstrap/docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`, `docs/exec-plans/canvas/`, `docs/references/` を root 運用 artefact として採用する
5. 反映後に `progress-log` と completed entries を再同期する
6. `MIGRATION_START_HERE.md` と `docs/migration/` を恒久運用にするか、移行完了後に archive するかを決める

## 並行運用ルール
- 本配置の直前まで、現行 `docs/` は source of truth のまま保つ
- 本配置は一括削除ではなく、backup を取ったうえで段階置換する
- `migration-bootstrap/` は本配置完了まで比較対象として残す
- `docs/exec-plans/completed/entries/` の履歴は失わない
- template と workflow reference は `docs/` 配下へ集約し、前プロジェクト固有の example は同梱しない

## 保護条件
- docs/
- AGENTS.md
- examples/
- `docs/exec-plans/completed/entries/`
- `tools/init_runner.py`
- `tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py`

## 本配置の完了条件
- root `AGENTS.md` と `docs/` が self-hosting 後の正本として揃う
- `docs/migration/` と `docs/templates/` が root に存在する
- root に `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`, `docs/exec-plans/canvas/`, `docs/references/` が置かれる
- `docs-builder.toml` が root manifest として残る
- rollback に必要な backup 先が残っている
