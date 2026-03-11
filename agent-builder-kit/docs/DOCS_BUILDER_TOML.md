# docs-builder.toml ガイド

## 目的
- `docs-builder.toml` は builder の正本入力
- 対話結果や質問票ではなく、最終的に採用した設定をここへ集約する

## 最初の一手
1. repo ルートに `docs-builder.toml` を新規作成する
2. `project`, `workflow`, `generation` を最低限埋める
3. `python3 tools/init_runner.py docs-builder.toml` を実行する

package には `docs-builder.toml.example` を同梱していない。最小構成はこの docs の項目一覧を見ながら手で作る。

## 最低限触る項目
### `[project]`
- `name`
- `slug`
- `mode`
- `request`

### `[workflow]`
- `profile`
- `role_model`
- `packs`

### `[generation]`
- `output_root`
- `overwrite_policy`

## よく使う組み合わせ
### 新規プロジェクト
```toml
[project]
mode = "new"

[workflow]
profile = "standard"
packs = ["obsidian_canvas_pack"]
```

### 既存プロジェクト移行
```toml
[project]
mode = "migration"

[workflow]
profile = "standard"
packs = ["migration_pack", "obsidian_canvas_pack"]

[migration]
current_state = "現行 docs の状態"
adoption_goal = "どう移行したいか"
existing_docs = ["README.md", "docs/old.md"]
```

### builder 自身の自己適用
```toml
[workflow]
packs = ["migration_pack", "obsidian_canvas_pack", "self_hosting_pack"]
```

- `self_hosting_pack` は builder 自身のメタ docs を source から引き継ぐ
- この repo 自身を dry-run するときは、まず `generation.output_root = "migration-bootstrap"` にする

## 迷ったら
- 完全仕様は [INPUT_SCHEMA.md](./INPUT_SCHEMA.md)
- 実行責務は [INIT_RUNNER.md](./INIT_RUNNER.md)
- 生成されるファイル群は [OUTPUT_PROFILES.md](./OUTPUT_PROFILES.md)

## init 後の扱い
- `docs-builder.toml` は init 後も残してよい
- 理由は、再実行、設定監査、他者への設定共有にそのまま使えるため
- 不要なら人間が手動で整理してよいが、`init_runner` が自動削除する前提にはしない
