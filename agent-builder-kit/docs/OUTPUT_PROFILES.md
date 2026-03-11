# Output Profiles

この docs は、C がどのファイル群を生成対象として持つかを固定するための仕様。

## 基本方針
- 出力は `profile` と `add-on pack` の組み合わせで決める。
- role model の違いでディレクトリ構成は増やさない。
- `4役標準` と `5役拡張` の違いは、主に `AGENTS.md` と workflow docs の文言差分で吸収する。
- 新規プロジェクト用と既存移行用は、共通骨格を持ちつつ `migration pack` だけ追加する。

## 共通骨格

すべての profile で最低限生成する。

- `AGENTS.md`
- `docs/index.md`
- `docs/PLANS.md`
- `docs/PRODUCT_SENSE.md`
- `docs/DESIGN.md`
- `docs/HUMAN_MANUAL.md`
- `docs/exec-plans/active/index.md`
- `docs/exec-plans/active/attention-queue.md`
- `docs/exec-plans/completed/index.md`
- `docs/exec-plans/completed/progress-log.md`
- `docs/exec-plans/completed/ENTRY_TEMPLATE.md`
- `docs/references/index.md`
- `docs/references/roles.md`
- `docs/references/lifecycle.md`
- `docs/references/review-policy.md`

## 共通 skill bundle

bootstrap 後の generated repo でも、package と同じ role skill asset を持つ。

- canonical role skill:
  - `tools/codex-skills/plan-manager/SKILL.md`
  - `tools/codex-skills/task-planner/SKILL.md`
  - `tools/codex-skills/task-worker/SKILL.md`
  - `tools/codex-skills/reviewer/SKILL.md`
- inventory:
  - `tools/codex-skills/README.md`
- support skill:
  - `tools/codex-skills/obsidian-canvas-sync/SKILL.md`
    - asset は package / generated repo に同梱する
    - ただし `obsidian_canvas pack` を有効にしたときだけ canvas docs / seed / sync 導線が activation される
  - `docs-sync`
    - 現時点では contract のみで未同梱
    - 実装する場合は `obsidian_canvas pack` の asset として ship する

## skill export 導線

- canonical source:
  - `tools/codex-skills/`
- user-facing export:
  - `.agents/skills/`
- current contract:
  - source repo と `agent-builder-kit` の正本は `tools/codex-skills/`
  - generated repo で `.agents/skills/` が存在する場合、利用者向け導線はそちらを優先してよい
  - `.agents/skills/` がない場合でも `tools/codex-skills/` だけで運用可能であることを崩さない
- implementation note:
  - `.agents/skills/` の物理 export は実装済み
  - generated repo では `tools/codex-skills/` と `.agents/skills/` の両方を出し、利用者向け入口を `.agents/skills/` へ寄せる

## reviewer handoff 契約

- `reviewer`
  - 役割:
    - code review 専用
    - コード、命名規則、フォールバック、境界逸脱、テスト不足を確認する
  - 起動条件:
    - `task-worker` がコード編集あり ticket を終えた直後
  - skip 条件:
    - markdown / docs 主体でコード編集がない ticket
    - ただし曖昧なら skip せず reviewer を優先する
  - asset 状態:
    - canonical asset として source / package / generated repo に載せる
  - alias 方針:
    - 旧 alias は package / generated repo に同梱しない

## Profile 定義

### 1. minimum
- 対象:
  - まず repo に運用骨格だけ入れたい
  - 既存プロジェクトへ小さく導入したい
  - docs の初期投資を抑えたい
- 含むもの:
  - 共通骨格のみ
- 意図:
  - 最低限の正本、進捗、review ルールを先に揃える

### 2. standard
- 対象:
  - plan / chunk / ticket まで docs 駆動で回したい
  - 曖昧な要求から task 化までの流れを固定したい
- 含むもの:
  - `minimum` のすべて
  - `docs/templates/project-intake-template.md`
  - `docs/templates/discovery-brief-template.md`
  - `docs/templates/plan-spec-template.md`
  - `docs/templates/chunk-sheet-template.md`
  - `docs/templates/ticket-template.md`
  - `docs/templates/fact-report-template.md`
  - `docs/templates/chunk-close-template.md`
  - 初期 seed block
- 意図:
  - B で定義した `intake -> discovery -> spec -> chunk -> ticket -> fact-report` を、そのまま運用可能にする

### 3. expanded
- 対象:
  - standard に加えて、設計や運用上の補助 docs も最初から持ちたい
  - プロジェクトの性質に応じて docs を増やしたい
- 含むもの:
  - `standard` のすべて
  - 必要な `add-on pack`
- 意図:
  - 1 つの巨大テンプレートではなく、必要な補助 docs だけ選べるようにする

## Add-on Pack

### migration pack
- 用途:
  - 既存プロジェクトへ後付け導入する
- 追加ファイル:
  - `MIGRATION_START_HERE.md`
  - `docs/migration/index.md`
  - `docs/migration/project-inventory.md`
  - `docs/migration/gap-report.md`
  - `docs/migration/adoption-plan.md`
  - `docs/migration/current-ai-migration-request.md`

### self_hosting pack
- 用途:
  - builder 自身の repo を、この builder で再構築検証したい
- 追加ファイル:
  - `README.md`
  - `docs/INPUT_SCHEMA.md`
  - `docs/OUTPUT_PROFILES.md`
  - `docs/DOCS_BUILDER_TOML.md`
  - `docs/INIT_RUNNER.md`
  - `docs/RENDERING_RULES.md`
- 備考:
  - 汎用 bootstrap docs に加えて、builder 自身のメタ設計 docs を source から引き継ぐ
  - source repo に builder 専用 active plan が存在する場合だけ、それを追加で継承する

### architecture pack
- 用途:
  - モジュール境界や責務分割を早めに固定したい
- 追加ファイル:
  - `docs/ARCHITECTURE.md`

### risk pack
- 用途:
  - セキュリティと信頼性の観点を正本として持ちたい
- 追加ファイル:
  - `docs/SECURITY.md`
  - `docs/RELIABILITY.md`

### ui pack
- 用途:
  - UI / frontend の設計メモを正本として持ちたい
- 追加ファイル:
  - `docs/FRONTEND.md`

### obsidian_canvas pack
- 用途:
  - Obsidian `.canvas` で plan / chunk / ticket の流れを可視化したい
- 追加ファイル:
  - `docs/OBSIDIAN_CANVAS_SYNC.md`
  - `docs/exec-plans/canvas/development-flow.canvas`
  - `docs/templates/block-note-template.md` または同等の block note 雛形
  - reference band の direct-source 本体 docs
    - `docs/PRODUCT_SENSE.md`
    - `docs/DESIGN.md`
    - `docs/HUMAN_MANUAL.md`
    - `docs/exec-plans/active/attention-queue.md`
  - 必要なら `docs/references/` の optional summary / hub note
- 配布契約:
  - `tools/codex-skills/obsidian-canvas-sync/SKILL.md` 自体は共通 skill bundle に含める
  - この pack は、その skill を有効に使うための docs / canvas / seed / sync 導線を追加する
  - 現時点では `docs-sync` support skill は同梱しない
  - ただし `docs-sync` を将来実装する場合、その ship 先はこの pack とし、reference band / hub docs を使わない profile へは配らない
  - したがって `obsidian_canvas pack` は「可視化」と「可視化に必要な summary sync」をまとめて有効化する境界とする

## role model と出力差分

### 4役標準
- 既定値
- `プランオーナー` を使う
- `project-intake` から `plan-spec` までを上流 1 役で持つ

### 5役拡張
- オプション
- `プランオーナー` を `プランマネージャー` と `仕様設計者` に分割する
- 追加ファイルは原則増やさない
- 役割名、owner 欄、workflow 説明だけを差し替える

## いま固定したこと
- C の標準出力 profile は `standard`
- C の既定 role model は `4役標準`
- `expanded` は `standard + add-on pack` として扱う
- 既存移行は別 profile ではなく `migration pack` の有無で表現する

## profile / pack smoke の最低確認
- package 自体には `tests/` を同梱しない
- source repo では `python3 tests/test_profile_pack_smoke.py` で major 組み合わせを回す
- package / generated repo 側では bootstrap verification と生成物確認で同じ観点を見る
- `standard + obsidian_canvas_pack`
  - `docs/exec-plans/canvas/development-flow.canvas` がある
  - `docs/migration/` と `docs/INIT_RUNNER.md` は出ない
- `migration_pack + obsidian_canvas_pack`
  - `MIGRATION_START_HERE.md` と `docs/migration/*.md` が出る
  - builder 固有の self-hosting docs は出ない
- `self_hosting_pack + obsidian_canvas_pack`
  - `docs/INPUT_SCHEMA.md`, `docs/OUTPUT_PROFILES.md`, `docs/DOCS_BUILDER_TOML.md`, `docs/INIT_RUNNER.md`, `docs/RENDERING_RULES.md` が出る
  - `agent-builder-kit` 単体展開でも `AGENTS.md` と `README.md` の fallback 生成で失敗しない

## まだ未確定のこと
- `minimum` でも `project-intake-template` を含めるべきか
- add-on pack の依存関係をどう表現するか
- 実際の builder 入力 schema で `profile` と `pack` をどう指定させるか
