# Design

## 設計方針
- A からは「運用の実例」を取る
- B からは「改善された責務分離と docs 受け渡し」を取る
- C では両者をそのまま複製せず、再利用可能な最小ルールへ落とす

## C の入力
- 正本入力は `docs-builder.toml`
- 対話型や質問票は入力収集レイヤーとして扱い、manifest へ正規化する
- schema の詳細は `INPUT_SCHEMA.md` を正本とする
- bootstrap の責務は `INIT_RUNNER.md` を正本とする

## C の出力
- profile に応じた `AGENTS.md` と `docs/` 一式
- 既定 profile は `standard`
- 既定 role model は `4役標準`
- 詳細なファイルセットは `OUTPUT_PROFILES.md` を正本とする
- manifest から docs への流し込み規則は `RENDERING_RULES.md` を正本とする
- Obsidian `.canvas` 連携は `obsidian_canvas_pack` で追加する
- 既存プロジェクト移行では `migration_pack` により `docs/migration/` と現行 AI 向け依頼文を追加する
- builder 自身の自己適用では `self_hosting_pack` によりメタ設計 docs を source から引き継ぐ
- 運用 phase の role skill 連携は `OPERATIONAL_SCHEMA.md` と `ROLE_SKILLS.md` を正本とする
- 初期 seed block を含む bootstrap 手順は `INIT_RUNNER.md` を正本とする

## 抽象化の境界
- 抽象化するもの
  - 役割
  - docs の責務分割
  - plan / chunk / ticket / review の流れ
  - 更新ルール
- 抽象化しないもの
  - 特定ドメイン語彙
  - 特定技術スタックの細部
  - 1 プロジェクト固有の仕様判断

## いまの前提
- A は参照資産として `examples/current-workflow-a/` に退避した
- B は template と reference を `docs/` 配下に集約し、package の重複 asset を増やさない
- C の正本はルート `docs/` と `AGENTS.md`

## 当面の設計課題
- `minimum` / `standard` / `expanded` と add-on pack の指定方法
- 新規プロジェクト用と移行用で何を共通化できるか
- テンプレート生成物の命名規則
- `.canvas` の JSON 更新を script 化するか skill 内で完結させるか
- role skill と validator をどこまで builder 出力へ含めるか
- `init_runner` の実装を Python script に固定するか

## reference summary との分担
- この file は本体 docs として扱う
- `docs/references/design.md` は canvas reference band 用の summary view とする
- 本体には設計方針、入力、出力、抽象化境界、設計課題を残す
- summary には短い見取り図だけを置き、仕様全文は持ち込まない
