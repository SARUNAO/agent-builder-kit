# Rendering Rules

この docs は、`docs-builder.toml` から生成先 docs へ何をどう流し込むかを定義する。

## 基本原則
- manifest が正本、生成された docs は render 結果とする
- 同じ manifest から再生成しても、同じ初期 docs 構造になることを優先する
- role model の違いはファイル差分ではなく文言差分で吸収する
- `.canvas` を含む可視化物も、docs と同じく manifest と運用 docs から再構築可能にする

## レンダリングの層

### 1. bootstrap render
- `docs-builder.toml` だけを元に初期 `AGENTS.md` と `docs/` を生成する
- プロジェクト開始時に 1 回行う

### 2. operational render
- 運用で更新された `project-intake`, `discovery-brief`, `plan-spec`, `chunk-sheet`, `ticket` から補助成果物を再同期する
- Obsidian `.canvas` はこの層に属する

## manifest からの流し込み規則

### `[project]`
- `project.name`
  - `docs/PRODUCT_SENSE.md` のタイトルと対象プロジェクト名へ入れる
- `project.request`
  - 初期 `project-intake` の要求原文へ入れる
- `project.summary`
  - `docs/PRODUCT_SENSE.md` の要約に入れる
- `project.primary_deliverable`
  - `docs/DESIGN.md` の前提と `project-intake` の成果物候補へ入れる

### `[workflow]`
- `workflow.profile`
  - 生成するファイル群を決める
- `workflow.role_model`
  - `AGENTS.md` と workflow docs の役割表現を切り替える
- `workflow.packs`
  - add-on pack の docs と assets を追加する
- `workflow.review_required`
  - `AGENTS.md` と review policy の既定文言へ入れる

### `[discovery]`
- `discovery.confirmed`
  - 初期 `discovery-brief` の確定事項
  - 初期 `plan-spec` の「人間に確認して確定した事項」
- `discovery.assumptions`
  - 初期 `discovery-brief` の仮置き前提
  - 初期 `plan-spec` の仮置き前提
- `discovery.non_goals`
  - 初期 `discovery-brief` と `plan-spec` の非目的
- `discovery.constraints`
  - 初期 `plan-spec` の制約

### `[migration]`
- migration pack 有効時のみ使う
- `migration.current_state`
  - `project-inventory` と `gap-report` の初期文面へ入れる
  - `current-ai-migration-request` の背景へ入れる
- `migration.adoption_goal`
  - `adoption-plan` の目的へ入れる
  - `current-ai-migration-request` の依頼目的へ入れる
- `migration.existing_docs`
  - `project-inventory` の既存 docs 棚卸しテーブルへ入れる
  - `current-ai-migration-request` の参照候補へ入れる
- `migration.known_gaps`
  - `gap-report` の初期論点へ入れる
- `migration.protected_paths`
  - `adoption-plan` の保護条件と `current-ai-migration-request` の禁止事項へ入れる
- `migration.notes`
  - `project-inventory` と `current-ai-migration-request` の補足へ入れる

## docs ごとの初期生成規則

### `AGENTS.md`
- `workflow.role_model` を反映
- `workflow.review_required` を反映
- `workflow.profile` に応じて読むべき docs を変える

### `docs/PRODUCT_SENSE.md`
- `project.name`, `project.summary`, `project.request` を元に初期化する

### `docs/DESIGN.md`
- `project.primary_deliverable`
- `workflow.profile`
- `workflow.packs`
- `project.mode`
  を元に初期前提を書く

### `docs/templates/project-intake-template.md`
- `project.request` をサンプル値または初期作成時の原文として流す

### `docs/templates/discovery-brief-template.md`
- `discovery.*` を初期項目へ展開する

### `docs/templates/plan-spec-template.md`
- `discovery.confirmed`, `discovery.assumptions`, `discovery.non_goals`, `discovery.constraints` を反映する

### `docs/templates/block-note-template.md`
- 常時必須ではない
- `obsidian_canvas_pack` が有効なときに補助ノートとして生成候補にする
- block の正本は引き続き `docs/exec-plans/plan-spec.md` の表に置く

### `docs/migration/project-inventory.md`
- `migration.current_state`
- `migration.existing_docs`
- `migration.notes`
  を元に初期棚卸し docs を作る

### `docs/migration/gap-report.md`
- `migration.current_state`
- `migration.known_gaps`
- `migration.adoption_goal`
  を元に初期差分 docs を作る

### `docs/migration/adoption-plan.md`
- `migration.adoption_goal`
- `migration.protected_paths`
  を元に段階導入 plan を作る

### `docs/migration/current-ai-migration-request.md`
- `migration.current_state`
- `migration.adoption_goal`
- `migration.existing_docs`
- `migration.protected_paths`
- `migration.notes`
  を元に、現行 AI へ渡す依頼文を作る

### `MIGRATION_START_HERE.md`
- migration pack 有効時のみ生成する
- `docs/migration/current-ai-migration-request.md` への入口として使う
- 現行 AI に「まずこれを読め」と明示する短いファイルにする
- 初手は `Step 1` のみ案内し、一度に全 step を走らせない

### self_hosting pack
- self-hosting pack 有効時のみ使う
- 汎用 render では足りない builder 自身のメタ docs を source から引き継ぐ
- 対象:
  - `AGENTS.md`
  - `README.md`
  - `docs/index.md`
  - `docs/PRODUCT_SENSE.md`
  - `docs/DESIGN.md`
  - `docs/PLANS.md`
  - `docs/INPUT_SCHEMA.md`
  - `docs/OUTPUT_PROFILES.md`
  - `docs/DOCS_BUILDER_TOML.md`
  - `docs/INIT_RUNNER.md`
  - `docs/RENDERING_RULES.md`
  - `docs/HUMAN_MANUAL.md`
- source repo に builder 専用 active plan が存在する場合だけ、それを追加継承する

## role model のレンダリング差分

### `four_role_default`
- `プランオーナー`
- `タスクプランナー`
- `タスクワーカー`
- `reviewer`

### `five_role_extended`
- `プランマネージャー`
- `仕様設計者`
- `タスクプランナー`
- `タスクワーカー`
- `reviewer`

差し替え対象:
- `AGENTS.md` の roles
- workflow docs の owner 名
- template の owner 欄

差し替えないもの:
- ファイル名
- ディレクトリ構成
- `ticket_id`, `chunk_id`, `block_id` の識別子ルール

## Obsidian canvas との関係
- `.canvas` は manifest から直接作らない
- `.canvas` は `docs/exec-plans/plan-spec.md`, `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md` など運用 docs を source of truth として再同期する
- そのため bootstrap render 後に operational sync を別段で持つ
- 詳細は `OBSIDIAN_CANVAS_SYNC.md` を正本とする
- `docs/exec-plans/blocks/*.md` は optional な補助ノートとして扱う
- managed node は text node を使い、補助ノートがあればタイトルを markdown link 化して参照できるようにする

## 再生成時の方針
- builder が生成した範囲だけを再描画対象にする
- 手編集を許す範囲と上書きする範囲を pack ごとに明示する
- `.canvas` では A/B/C の予約レーン内は再配置対象、予約外ノートは保持対象とする

## まだ未確定のこと
- discovery の空配列を docs に空欄で出すか、節ごと省略するか
- 初回 render と再 render でテンプレートコメントを残すかどうか
- migration 時の seed block を new と完全に分岐させるか、discovery 共通に寄せるか
