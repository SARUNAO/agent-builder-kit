# Builder Package Contents

このディレクトリは、新規の空プロジェクトへ持っていく最小パッケージ。

## 境界
- package assets の正本をここに置く
- bootstrap 後に生成される runtime artefact はここへ含めない
- runtime artefact の整理方針は [docs/BOOTSTRAP_LAYOUT.md](./docs/BOOTSTRAP_LAYOUT.md) を参照する

## 含めたもの
- `README.md`
- `tools/`
- `docs/`

## 同梱 skill bundle
- canonical role skill:
  - `tools/codex-skills/plan-manager/SKILL.md`
  - `tools/codex-skills/task-planner/SKILL.md`
  - `tools/codex-skills/task-worker/SKILL.md`
  - `tools/codex-skills/reviewer/SKILL.md`
- inventory:
  - `tools/codex-skills/README.md`
- user-facing export:
  - package 自体には `.agents/skills/` を同梱しない
  - bootstrap 後の generated repo では `.agents/skills/` に同じ skill bundle を export する
  - `tools/codex-skills/` は package / generated の両方で canonical source として残す
- optional workflow support:
  - `tools/codex-skills/obsidian-canvas-sync/SKILL.md`
    - asset 自体は同梱する
    - ただし実際に canvas docs / seed / sync 導線を生成するのは `obsidian_canvas pack` 有効時だけ
- 未同梱:
  - `docs-sync`
    - まだ contract のみで、package asset には入れていない

## 同梱の参照資産
- `docs/references/` に workflow / role / review reference を同梱する
- `docs/templates/` に planning template の正本を同梱する
- `docs/migration/` は package 自身の self-hosting migration 履歴 / handoff note として暫定同梱する
- `examples/current-workflow-a/` のような前プロジェクト固有資料は同梱しない

`docs/migration/` は generic generated repo の migration docs 正本そのものではなく、archive 退避先が確定するまで package 内に保持している履歴 note として扱う。

## 含めていないもの
- `.agents/skills/` の package mirror
- `examples/`
- `backup/`
- `migration-bootstrap/`
- builder 固有の active queue、active plan、completed history
- builder 固有の source reference 台帳
- bootstrap 後の runtime artefact
  - `docs/exec-plans/project-intake.md`
  - `docs/exec-plans/discovery-brief.md`
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/blocks/`
  - `docs/exec-plans/chunks/`
  - `docs/exec-plans/tickets/`
  - `docs/exec-plans/fact-reports/`
  - `docs/exec-plans/canvas/`
  - `docs/references/`

## 既定の出力契約
- runtime planning artefact は `docs/exec-plans/` 配下へ出力する
- reference は `docs/references/` 配下へ出力する
- `canvas` は `docs/exec-plans/canvas/` 配下へ置く
- 旧レイアウトを使いたい場合だけ `generation.planning_root = "."` と明示 override する

## 使い方
1. 新規プロジェクトのルートへ `agent-builder-kit/` ディレクトリをそのまま置く
2. `agent-builder-kit/docs/DOCS_BUILDER_TOML.md` を見て、repo ルートに `docs-builder.toml` を作成して編集する
3. `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml` を実行する
4. init 後、AI は人間に `agent-builder-kit/` を残すか削除するか確認する
5. 既定は保持で、削除したい場合だけ `--cleanup-package` 付きで再実行するか、人間が手動削除する

## Codex アプリでの再読込
- skill bundle は展開しただけでは Codex アプリに即時認識されないことがある
- generated repo で skill を使う前に、いったん現在のスレッドを閉じる
- Codex アプリを再起動し、展開した project を新しい project として開き直す
- 開き直し後に `AGENTS.md` と `docs/HUMAN_MANUAL.md` を読み、`plan-manager` から開始する

## bootstrap 後の確認ポイント
- `docs/index.md` から主要 docs に辿れること
- `docs/exec-plans/plan-spec.md` と `docs/exec-plans/blocks/` が生成されていること
- `docs/references/` に reference band 用の seed が生成されていること
- `docs/exec-plans/active/attention-queue.md` が cluster 名ベースの static cleanup review seed で始まること
- `tools/codex-skills/` に canonical role skill が揃っていること
- generated repo に `.agents/skills/` が export され、利用者向け入口として読めること
- code ticket は `task-worker` 後に reviewer を呼ぶ前提で docs を読めること
- markdown / docs 主体 ticket は docs-only skip 条件を明示すれば reviewer を省略できること
