# Input Schema

この docs は、C の builder が受け取る入力の正本 schema を定義する。

## 結論
- builder の正本入力は質問票そのものではなく manifest file にする。
- 質問票や対話は入力収集レイヤーとして扱い、最終的に manifest へ正規化する。
- manifest の既定形式は `TOML` とする。
- 既定ファイル名はルートの `docs-builder.toml` とする。
- 利用開始時は `docs-builder.toml.example` を雛形として使う。

## なぜ manifest を正本にするか
- 再生成時に同じ入力を再利用しやすい
- 対話型 UI がなくても CLI や手編集で扱える
- 既存プロジェクト移行時に差分比較しやすい
- 「何を聞いたか」ではなく「最終的に何を採用したか」を残せる

## 質問票との関係
- 質問票は `input acquisition layer`
- manifest は `canonical source of truth`
- 対話型 builder は、質問結果を manifest に変換して保存する
- 非対話型 builder は、manifest を直接読む

## schema の層

### 1. project layer
- このプロジェクトが何者か
- 新規作成か既存移行か
- 何を作りたいのか

### 2. workflow layer
- どの role model と profile を採用するか
- どの docs pack を出力するか

### 3. discovery layer
- 要求原文
- 確定事項
- 仮置き前提
- 非目的
- 制約

### 4. migration layer
- 既存プロジェクト移行時だけ必要
- 現在ある docs / 運用 / repo 状態

### 5. obsidian layer
- Obsidian `.canvas` 連携時の設定
- vault と canvas の配置
- 自動同期のトリガー

### 6. bootstrap layer
- 初期 skeleton をどこまで生成するか
- seed block を入れるか
- 初期 reference note を何にするか

## 必須フィールド

### 常に必須
- `schema_version`
- `project.name`
- `project.slug`
- `project.mode`
- `project.request`
- `workflow.profile`
- `workflow.role_model`

### `project.mode = "migration"` のとき必須
- `migration.current_state`
- `migration.adoption_goal`
- `migration.existing_docs`

## 推奨フィールド
- `project.summary`
- `project.primary_deliverable`
- `project.target_users`
- `workflow.packs`
- `workflow.review_required`
- `bootstrap.seed_discovery_block`
- `bootstrap.reference_seed`
- `discovery.confirmed`
- `discovery.assumptions`
- `discovery.non_goals`
- `discovery.constraints`
- `migration.known_gaps`
- `migration.protected_paths`
- `migration.notes`

## TOML 形状

```toml
schema_version = 1

[project]
name = "Bitcoin Insight Dashboard"
slug = "bitcoin-insight-dashboard"
mode = "new"
request = "ビットコインの価格と、関連するニュースをフィードするダッシュボードを作りたい"
summary = "BTC の価格監視とニュース把握を 1 画面で行う dashboard"
primary_deliverable = "web_dashboard"
target_users = ["crypto_trader", "market_watcher"]

[workflow]
profile = "standard"
role_model = "four_role_default"
packs = ["ui_pack", "obsidian_canvas_pack"]
review_required = true

[bootstrap]
seed_discovery_block = true
reference_seed = ["product_sense", "design", "attention_queue", "human_manual"]

[obsidian]
vault_root = "/path/to/obsidian-vault"
reserve_manual_lane = true
sync_on_chunk_close = true

[discovery]
confirmed = [
  "MVP は Web dashboard",
  "対象銘柄は Bitcoin のみ"
]
assumptions = [
  "価格更新は 1 分間隔でよい",
  "関連ニュースは BTC キーワード一致でよい"
]
non_goals = [
  "売買機能",
  "ポートフォリオ管理"
]
constraints = [
  "無料または低コストの API から始める",
  "初期段階では認証なし"
]

[generation]
output_root = "."
planning_root = "planning"
overwrite_policy = "safe_merge"
include_examples = false
```

## 列挙値

### `project.mode`
- `new`
- `migration`

### `workflow.profile`
- `minimum`
- `standard`
- `expanded`

### `workflow.role_model`
- `four_role_default`
- `five_role_extended`

### `workflow.packs`
- `migration_pack`
- `self_hosting_pack`
- `architecture_pack`
- `risk_pack`
- `ui_pack`
- `obsidian_canvas_pack`

### `generation.overwrite_policy`
- `safe_merge`
- `replace_generated_only`

## セクション定義

### `[project]`
- 役割:
  - intake の入口情報を保持する
- 目的:
  - 何のための repo かを builder が理解する

必須:
- `name`
- `slug`
- `mode`
- `request`

任意:
- `summary`
- `primary_deliverable`
- `target_users`
- `notes`

### `[workflow]`
- 役割:
  - どの運用フローを生成するかを決める

必須:
- `profile`
- `role_model`

任意:
- `packs`
- `review_required`
- `parallelism_hint`

### `[discovery]`
- 役割:
  - `project.request` を仕様化前に整形した情報を入れる
- 備考:
  - 空でもよいが、`standard` 以上では記入を推奨する

任意:
- `confirmed`
- `assumptions`
- `open_questions`
- `non_goals`
- `constraints`
- `success_criteria`

### `[migration]`
- 役割:
  - 既存プロジェクトへの後付け導入に必要な現状把握
- 条件:
  - `project.mode = "migration"` のときのみ使う

必須:
- `current_state`
- `adoption_goal`
- `existing_docs`

任意:
- `known_gaps`
- `protected_paths`
- `notes`

これらは migration pack の初期 docs と `current-ai-migration-request` のガードレールへ流し込める。

### `[obsidian]`
- 役割:
  - Obsidian `.canvas` 連携の設定を持つ
- 条件:
  - `workflow.packs` に `obsidian_canvas_pack` を含むときに使う

推奨:
- `reference_dir`
  - 上段中央の reference band に置く参照 note ディレクトリ

推奨:
- `vault_root`
- `canvas_path`
- `reserve_manual_lane`
- `sync_on_chunk_close`

補足:
- `canvas_path` と `reference_dir` を省略した場合は、`generation.planning_root` に従って既定パスを解決する

### `[bootstrap]`
- 役割:
  - `init_runner` が置く初期 skeleton を制御する

推奨:
- `seed_discovery_block`
  - 初期 block として `何を作るか決める` を生成するか
- `reference_seed`
  - 初期 `docs/references/` に何を置くか

### `[generation]`
- 役割:
  - 生成時の実行オプション

任意:
- `output_root`
- `planning_root`
- `overwrite_policy`
- `include_examples`

## builder の動き

1. 質問票または対話で情報を集める
2. 収集した情報を `docs-builder.toml` に正規化する
3. manifest を検証する
4. `profile` と `packs` に応じて生成対象を決める
5. `role_model` に応じて文言差分を適用する
6. `project` と `discovery` の内容を初期 docs へ流し込む
7. `bootstrap.seed_discovery_block = true` なら、`何を作るか決める` block を初期 seed として置く
8. `obsidian_canvas_pack` が有効なら、canvas sync 用 docs と skill bundle を生成する
9. `bootstrap.reference_seed` があれば、初期 `docs/references/` を生成する
10. `project.mode = "migration"` または `migration_pack` が有効なら、`docs/migration/` と現行 AI 向け依頼文を生成する

## Bitcoin dashboard 例での読み替え
- `project.request`
  - 「ビットコインの価格と、関連するニュースをフィードするダッシュボードを作りたい」
- `workflow.profile`
  - `standard`
- `workflow.role_model`
  - `four_role_default`
- `workflow.packs`
  - `["ui_pack", "obsidian_canvas_pack"]`
- `discovery.confirmed`
  - `MVP は Web dashboard`
- `discovery.assumptions`
  - `関連ニュースは BTC キーワード一致でよい`

## いま固定したこと
- 質問票は正本にしない
- manifest を正本にする
- 既定 manifest 形式は `TOML`
- 既定ファイル名は `docs-builder.toml`

## まだ未確定のこと
- `parallelism_hint` のような運用補助フィールドをどこまで schema に含めるか
- `generation` を schema 本体に含めるか、CLI option に逃がすか
- manifest から初期 `project-intake` と `discovery-brief` をどうレンダリングするか
- Obsidian vault 外部パスをどこまで許可するか
