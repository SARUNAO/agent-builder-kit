# Current AI Migration Request

- request_id: MIGRATION-REQUEST-2026-03-09
- related_plan: PLAN-2026-03-09-DOCS-BUILDER
- status: ready
- owner: プランオーナー
- last_updated: 2026-03-09

あなたはこのプロジェクトの現行 docs / 運用を把握している AI です。  
以下の migration bootstrap を参照し、既存運用を新 schema へ写像してください。

## 目的
- 既存運用を保ったまま、この repo 自身が docs_builder の生成物でも再現できることを確認する。

## 現在の運用前提
- この repo には既に docs/ と AGENTS.md があり、builder 自身の正本として運用している。まずは既存 docs を壊さずに migration-bootstrap を別出力で生成し、差分を確認したい。

## 参照するもの
- `docs/migration/project-inventory.md`
- `docs/migration/gap-report.md`
- `docs/migration/adoption-plan.md`
- `docs/OPERATIONAL_SCHEMA.md`
- `docs/ROLE_SKILLS.md`

## 既存 docs 候補
- AGENTS.md
- docs/index.md
- docs/PLANS.md
- docs/PRODUCT_SENSE.md
- docs/DESIGN.md
- docs/INPUT_SCHEMA.md
- docs/INIT_RUNNER.md
- docs/OPERATIONAL_SCHEMA.md
- docs/ROLE_SKILLS.md
- docs/OBSIDIAN_CANVAS_SYNC.md

## 進め方
### Step 1
- 既存 docs と運用 artefact を棚卸しし、`docs/migration/project-inventory.md` を埋める
- この step が終わったら、まだ次の step を実行せず、棚卸し結果を返す

### Step 2
- `docs/migration/project-inventory.md` を元に、現在の flow を `block / chunk / ticket` 相当へ写像する
- 差分と open question を `docs/migration/gap-report.md` へ反映する
- この step が終わったら、差分結果を返す

### Step 3
- `docs/migration/gap-report.md` を元に、導入順を `docs/migration/adoption-plan.md` に段階化する
- 人間承認が必要な判断と protected path を明示する
- この step が終わったら、導入 plan を返す

## 禁止事項
- docs/
- AGENTS.md
- docs/templates/
- examples/

## 返してほしいもの
- Step 1 完了時: 埋まった `docs/migration/project-inventory.md`
- Step 2 完了時: 埋まった `docs/migration/gap-report.md`
- Step 3 完了時: 埋まった `docs/migration/adoption-plan.md`
- 残っている open question

## 補足
- 最初の適用は本配置ではなく migration-bootstrap への dry-run とする
