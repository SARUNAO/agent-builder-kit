# docs_builder

AI コーディング前提の開発フローを初期化する `AGENTS.md` と `docs/` 一式を生成するビルダー。

## 入口
- 設計の正本: [docs/index.md](./docs/index.md)
- 使い方の入口: [docs/INIT_RUNNER.md](./docs/INIT_RUNNER.md)
- 人間向け運用ガイド: [docs/HUMAN_MANUAL.md](./docs/HUMAN_MANUAL.md)
- 配置整理の方針: [docs/BOOTSTRAP_LAYOUT.md](./docs/BOOTSTRAP_LAYOUT.md)
- `docs-builder.toml` の説明: [docs/DOCS_BUILDER_TOML.md](./docs/DOCS_BUILDER_TOML.md)
- docs の phase 別メモ: [docs/DOCS_LIFECYCLE.md](./docs/DOCS_LIFECYCLE.md)
- release gate: [docs/ACCEPTANCE_MATRIX.md](./docs/ACCEPTANCE_MATRIX.md)
- 設定ガイド: [docs/DOCS_BUILDER_TOML.md](./docs/DOCS_BUILDER_TOML.md)

## 最短手順
1. 新しい repo に `agent-builder-kit/` ディレクトリのまま持ち込む
2. [docs/DOCS_BUILDER_TOML.md](./docs/DOCS_BUILDER_TOML.md) を見て、repo ルートに `docs-builder.toml` を作成して調整する
3. `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml` を実行する
3. 生成された `AGENTS.md`, `docs/`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/`, `docs/exec-plans/canvas/` を確認する
4. `docs/exec-plans/active/attention-queue.md` に cluster 名ベースの初期 cleanup reminder が入っていることを確認する
5. `docs/HUMAN_MANUAL.md` を開き、`plan-manager -> task-planner -> task-worker` の順で進める

## 人間向けの最短導線
1. [docs/HUMAN_MANUAL.md](./docs/HUMAN_MANUAL.md) を開く
2. `plan-manager` にやりたいことを伝え、仕様確認とおすすめを出してもらう
3. `task-planner` に chunk / ticket を切ってもらう
4. `docs/exec-plans/canvas/development-flow.canvas` を見ながら `task-worker` に実装を進めてもらう

## 生成後に出力されるもの
- `AGENTS.md`
- `docs/`
- runtime planning artefact
  - `docs/exec-plans/project-intake.md`
  - `docs/exec-plans/discovery-brief.md`
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/`
- `tools/codex-skills/`
- `.agents/skills/`
- 必要なら `docs/exec-plans/canvas/development-flow.canvas`

## Human Flow
- やりたいことや違和感は、まず `plan-manager` に伝える
- block に入る前の仕様詰めとおすすめ提示も `plan-manager` に任せる
- 実装単位の整理と `done` 判断は `task-planner` に任せる
- 実装は `task-worker`、コード変更があるなら後段 review は `reviewer`
- 1 block 進んだら `docs/DOCS_LIFECYCLE.md` を見て、常時見なくてよい docs を確認する

## Codex アプリ利用時の注意
- skill はファイルを展開しただけでは Codex アプリに即時認識されないことがある
- bootstrap 後に生成された project で skill を使う前に、いったん現在のスレッドを閉じる
- その後 Codex アプリを再起動し、展開した project を新しい project として開き直す
- 開き直したあとに `AGENTS.md` と `docs/HUMAN_MANUAL.md` を入口として作業を始める

## package に含めないもの
- builder 固有の active queue や active plan
- builder 固有の completed history
- builder 固有の source reference 台帳

## いま見えている整理方針
- package assets と runtime artefact は別物として扱う
- runtime planning artefact は `docs/exec-plans/` 配下へ集約する
- human-facing reference は `docs/references/` 配下へ集約する
- package 自体の skill 正本は `tools/codex-skills/` に置き、`.agents/skills/` は generated repo 側でだけ作る
- 詳細は [docs/BOOTSTRAP_LAYOUT.md](./docs/BOOTSTRAP_LAYOUT.md) を正本とする

## init 後の扱い
- `docs-builder.toml` は再実行と設定監査のため保持を既定とする
- 展開に使った `agent-builder-kit/` は既定では残す
- AI は init 後に人間へ「展開元の `agent-builder-kit/` を残すか削除するか」を確認する
- 削除したい場合だけ `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml --cleanup-package` を使うか、人間が手動で削除してよい

## モード
- `project.mode = "new"`
  - 新規プロジェクトを bootstrap する
- `project.mode = "migration"`
  - 既存プロジェクト移行用の `docs/migration/` と `MIGRATION_START_HERE.md` を含めて生成する

## package 内 migration docs の扱い
- `agent-builder-kit/docs/migration/` は package 自身の self-hosting 履歴 / handoff note であり、generic package canonical の常設 docs とは切り分けて扱う
- archive 退避先が確定するまでは package 内に保持するが、方針上は package canonical から外して archive へ寄せる前提とする
