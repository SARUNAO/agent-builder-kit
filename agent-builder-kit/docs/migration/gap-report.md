# Gap Report

- gap_report_id: GAP-2026-03-09
- related_plan: PLAN-2026-03-09-DOCS-BUILDER
- status: done
- owner: プランオーナー
- last_updated: 2026-03-09

## package 内での位置づけ
- この file は package 自身の self-hosting migration 履歴 / handoff note
- generic generated repo の migration docs 正本ではない
- archive 退避先が確定したら package canonical から外す前提で保持している

## 移行目的
- 既存運用を保ったまま、この repo 自身が docs_builder の生成物でも再現できることを確認する。

## 現在の運用要約
- この repo には既に docs/ と AGENTS.md があり、builder 自身の正本として運用している。まずは既存 docs を壊さずに migration-bootstrap を別出力で生成し、差分を確認したい。
- `self_hosting_pack` を入れたことで、builder 固有 docs の大部分は source から引き継げるようになった。
- 現時点の意図した差分は、migration 作業台と generated template 群、および dry-run 実行後に増えた progress 履歴へ寄っている。

## Mapping Summary
| current_item | target_item | gap_type | required_action | owner | notes |
|---|---|---|---|---|---|
| `docs/` core docs | `migration-bootstrap/docs/` | resolved_by_self_hosting | self_hosting pack で source 継承を維持する | plan-owner | `AGENTS.md`, `PRODUCT_SENSE`, `DESIGN`, `PLANS`, `INPUT_SCHEMA` などは大差分を解消済み |
| `docs/references/` | `migration-bootstrap/docs/references/` | resolved_by_self_hosting | source 継承を維持する | plan-owner | 現在は一致 |
| `docs/exec-plans/` | `migration-bootstrap/docs/exec-plans/` | runtime_drift | 本配置前に progress と completed entries の同期方針を決める | plan-owner | dry-run 後の entry 追加で差分が再発する |
| 既存 repo 直下に存在しない `docs/migration/` | `migration-bootstrap/docs/migration/` | additive | migration 作業台として追加するか、一時運用に留めるか決める | plan-owner | 現在の主要差分 |
| 既存 repo 直下に存在しない `docs/templates/` | `migration-bootstrap/docs/templates/` | additive | builder 配布用 template 群として採用するか決める | plan-owner | 現在の主要差分 |
| `docs/DOCS_BUILDER_TOML.md` | `migration-bootstrap/docs/DOCS_BUILDER_TOML.md` | source_ahead | 生成前後で最新化タイミングを揃える | plan-owner | self_hosting pack 追加後の説明差分が未再反映 |
| `README.md` と root manifest 群 | `migration-bootstrap/README.md`, `docs-builder.toml` 系 | partial_adoption | 本配置で root artefact をどこまで正式採用するか決める | plan-owner | 生成物はあるが現行 root と共存中 |
| `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`, `docs/exec-plans/canvas/`, `docs/references/` | generated planning runtime | additive_runtime | self migration の本配置時に正式運用へ入れるか決める | task-planner | dry-run では作業台として追加されている |

## open question
- `docs/migration/` は本配置後も恒久的に残すか、それとも移行完了後に archive するか
- `docs/templates/` をこの repo 自身の正本にも含めるか、それとも builder 配布時だけの artefact として扱うか
- `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`, `docs/exec-plans/canvas/`, `docs/references/` を self-hosting 後の正式運用へ昇格させるか
- dry-run 後に増える `progress-log` と completed entries を、本配置比較のたびにどう同期するか
- `docs-builder.toml` はこの repo の恒久 root artefact として保持する契約で確定したため、cleanup 可否の再検討は不要。必要なら記述の所在だけを整理する

## 人間確認が必要な判断
- 現行 `docs/` を `backup/` へ退避するタイミング
- `migration-bootstrap/` を本配置候補としてどこまで信頼するか
- `docs/migration/` と `docs/templates/` を正式採用するか
- root に `MIGRATION_START_HERE.md` を本配置でも残すか

## 次アクション
- Step 3 として `migration-bootstrap/docs/migration/adoption-plan.md` に導入順を段階化する
- 本配置前に `docs/DOCS_BUILDER_TOML.md` の最新差分を migration-bootstrap 側へ再反映するか決める

## 補足
- cleanup 契約の current source of truth は `README.md`, `docs/index.md`, `docs/DOCS_BUILDER_TOML.md`, `docs/BOOTSTRAP_LAYOUT.md` とし、この gap report は移行論点の履歴として扱う
