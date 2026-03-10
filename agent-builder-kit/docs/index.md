# Docs Hub

## Core
- [PLANS.md](./PLANS.md)
- [PRODUCT_SENSE.md](./PRODUCT_SENSE.md)
- [DESIGN.md](./DESIGN.md)
- [BOOTSTRAP_LAYOUT.md](./BOOTSTRAP_LAYOUT.md)
- [DOCS_LIFECYCLE.md](./DOCS_LIFECYCLE.md)
- [OUTPUT_PROFILES.md](./OUTPUT_PROFILES.md)
- [INPUT_SCHEMA.md](./INPUT_SCHEMA.md)
- [DOCS_BUILDER_TOML.md](./DOCS_BUILDER_TOML.md)
- [INIT_RUNNER.md](./INIT_RUNNER.md)
- [HUMAN_MANUAL.md](./HUMAN_MANUAL.md)
- [ACCEPTANCE_MATRIX.md](./ACCEPTANCE_MATRIX.md)
- [OPERATIONAL_SCHEMA.md](./OPERATIONAL_SCHEMA.md)
- [ROLE_SKILLS.md](./ROLE_SKILLS.md)
- [RENDERING_RULES.md](./RENDERING_RULES.md)
- [OBSIDIAN_CANVAS_SYNC.md](./OBSIDIAN_CANVAS_SYNC.md)

## Execution
- [exec-plans/active/index.md](./exec-plans/active/index.md)
- [exec-plans/active/attention-queue.md](./exec-plans/active/attention-queue.md)
- [exec-plans/completed/progress-log.md](./exec-plans/completed/progress-log.md)

## Human Flow
- [HUMAN_MANUAL.md](./HUMAN_MANUAL.md) から始める
- `plan-manager` に目的と追加要件を伝える
- `task-planner` に chunk / ticket を切ってもらう
- `task-worker` に実装してもらい、`task-planner` に `done` 判断をしてもらう
- generated repo で `obsidian_canvas_pack` が有効なら `exec-plans/canvas/development-flow.canvas` を見ながら block -> chunk -> ticket の順で進める

## Migration
- [migration/index.md](./migration/index.md)

## Templates
- [templates/index.md](./templates/index.md)

## References
- [references/index.md](./references/index.md)

## Optional Inputs
- `examples/current-workflow-a/README.md` のような前プロジェクト資料は package に同梱しない
- 必要なら利用者が別途持ち込んだ参照資料として扱う

## Post-init Notes
- `docs-builder.toml` は bootstrap の正本入力として残してよい
- 展開元の `agent-builder-kit/` は保持してもよく、不要なら人間が手動で削除してよい
- 自動 cleanup は行わない
