# Project Inventory

- inventory_id: INVENTORY-2026-03-09
- related_plan: PLAN-2026-03-09-DOCS-BUILDER
- status: done
- owner: プランオーナー
- last_updated: 2026-03-09

## package 内での位置づけ
- この file は package 自身の self-hosting migration 履歴 / handoff note
- generic generated repo の migration docs 正本ではない
- archive 退避先が確定したら package canonical から外す前提で保持している

## 現在の運用要約
- この repo には既に docs/ と AGENTS.md があり、builder 自身の正本として運用している。まずは既存 docs を壊さずに migration-bootstrap を別出力で生成し、差分を確認したい。
- source of truth はルート `AGENTS.md`, `docs/`, `docs/exec-plans/`, `docs/references/` で、template / reference asset も `docs/` 配下に集約されている。
- builder 本体の実装は `tools/init_runner.py` と `tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py` を中心に持ち、docs 設計と実装が同一 repo に共存している。
- runtime planning artefact は `docs/exec-plans/` 配下で管理し、reference band は `docs/references/` を正本とする。

## 既存 docs / artefact 棚卸し
| path_or_location | kind | current_role | keep_or_replace | notes |
|---|---|---|---|---|
| AGENTS.md | agent_hub | workspace の正本ハブ | keep | A/B/C 境界、bootstrap、運用規則を定義 |
| README.md | project_entry | 人間向け入口 | keep | 利用開始時の導線 |
| docs/index.md | docs_hub | docs 正本の入口 | keep | core / execution / references / external inputs を束ねる |
| docs/PRODUCT_SENSE.md | core_doc | builder 自身の価値仮説 | keep | 汎用 scaffold ではなく自己記述 docs |
| docs/DESIGN.md | core_doc | builder 自身の設計方針 | keep | A/B/C 抽象化境界を持つ |
| docs/PLANS.md | plan_hub | runtime planning への入口 | keep | 現在の active plan 正本は `docs/exec-plans/plan-spec.md` に置く |
| docs/INPUT_SCHEMA.md | builder_meta | manifest 正本 schema | keep | builder 固有 docs |
| docs/OUTPUT_PROFILES.md | builder_meta | 出力 profile 定義 | keep | builder 固有 docs |
| docs/DOCS_BUILDER_TOML.md | builder_meta | manifest の利用ガイド | keep | 利用者向け説明 |
| docs/INIT_RUNNER.md | builder_meta | bootstrap 責務 | keep | init_runner の仕様 |
| docs/RENDERING_RULES.md | builder_meta | render 規則 | keep | manifest -> docs 変換規則 |
| docs/OPERATIONAL_SCHEMA.md | runtime_schema | 運用時 schema | keep | role skill と更新責務の正本 |
| docs/ROLE_SKILLS.md | runtime_schema | role skill 連携 | keep | plan-owner / task-planner / task-worker-reviewer |
| docs/OBSIDIAN_CANVAS_SYNC.md | runtime_schema | `.canvas` 同期設計 | keep | add-on pack の正本 |
| docs/HUMAN_MANUAL.md | runtime_doc | 人間判断の基準 | keep | 承認・禁止事項の入口 |
| docs/references/index.md + `roles/lifecycle/review-policy` | reference_doc | 共通 reference set | keep | runtime reference は `docs/references/` に置く |
| docs/exec-plans/active/index.md + attention-queue.md | active_exec | active queue の入口 | keep | current workspace では空 seed を維持 |
| docs/exec-plans/completed/index.md + progress-log.md | completed_exec | completed digest の入口 | keep | current workspace では空 seed を維持 |
| docs/exec-plans/ | runtime_planning | planning artefact 一式 | keep | `project-intake`, `discovery-brief`, `plan-spec`, `blocks`, `chunks`, `tickets`, `fact-reports`, `canvas`, `active`, `completed` を含む |
| docs/references/ | runtime_reference | reference band 一式 | keep | canvas 参照と role skill が読む runtime reference の正本 |
| docs/templates/ | template_asset | planning template 群 | keep | package 内の template source |
| docs/references/*.md | reference_asset | workflow / role / review reference | keep | package 単体でも参照可能 |
| tools/init_runner.py | implementation | bootstrap 実装本体 | keep | builder の実行入口 |
| tools/codex-skills/ | implementation | role skill / canvas skill | keep | 出力対象でもある |
| docs-builder.toml | manifest | self migration 用入力正本 | keep | この repo 自身の dry-run 設定 |
| docs-builder.toml.example | manifest_example | 利用者向け雛形 | keep | 新規利用者の入口 |
| migration-bootstrap/ | generated_dry_run | self migration の検証出力 | keep_for_review | 本配置前の比較対象 |

## 現在の flow mapping
| current_unit | observed_meaning | target_schema | notes |
|---|---|---|---|
| AGENTS.md | workspace 全体のハブと規約 | AGENTS.md | self_hosting では source 継承が必要 |
| docs/index.md | core docs のルーティング | docs/index.md | builder 固有リンクを維持する必要がある |
| docs/PRODUCT_SENSE.md + docs/DESIGN.md | builder 自身の価値仮説と設計 | docs/PRODUCT_SENSE.md + docs/DESIGN.md | 汎用 scaffold へ置換すると情報が落ちる |
| docs/PLANS.md + docs/exec-plans/plan-spec.md | active plan hub と runtime planning | docs/PLANS.md + docs/exec-plans/* | `docs/PLANS.md` は入口、正本は `docs/exec-plans/` に置く |
| docs/exec-plans/completed/* | completed digest | docs/exec-plans/completed/* | generic seed を維持し、runtime 履歴の正本とは分離する |
| docs/templates/* | 生成元 template 群 | docs/templates/* | 生成先では同じ path 契約でコピーされる |
| tools/init_runner.py | bootstrap 実装 | tools/init_runner.py | 実装本体として維持 |
| tools/codex-skills/obsidian-canvas-sync | 可視化 add-on 実装 | tools/codex-skills/obsidian-canvas-sync | script + skill の構成を維持 |
| migration-bootstrap/docs/migration/* | migration の作業台 | docs/migration/* | self migration では追加差分として許容 |

## 保護すべきもの
- docs/
- AGENTS.md
- `docs/exec-plans/completed/entries/` の履歴
- `tools/init_runner.py` と `tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py` の実装本体

## 未把握事項
- `migration-bootstrap/` を本配置へ昇格するとき、`docs/exec-plans/active/`, `docs/exec-plans/completed/`, `docs/exec-plans/fact-reports/` をどこまで比較対象に含めるか
- `docs/migration/` を最終的に恒久 docs として残すか、一時作業台として扱うか
- self-hosting pack の対象に `README.md` 以外の root artefact を追加すべきか

## 次アクション
- Step 2 として `migration-bootstrap/docs/migration/gap-report.md` に差分と open question を整理する
- 本配置前に `migration-bootstrap/` と現行 `docs/` の差分を review し、意図した差分だけか確認する

## 補足
- 最初の適用は本配置ではなく migration-bootstrap への dry-run とする
- self_hosting_pack を入れたことで、builder 固有 docs の差分は `migration/` と `templates/` へほぼ限定できている
