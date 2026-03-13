---
reference_id: REF-DESIGN
title: Design
lane_order: 200
owner_role: plan_owner
sync_mode: direct_source
kind: reference_source
---

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

## `conductor` backport の境界
- generic な orchestration asset を同梱する場合、runtime asset の正本は `tools/conductor/` を新設して置く
- 想定する対象は `flow_conductor.py`, `run_conductor.sh`, `add_operator_request.sh`, 及びそれを説明する契約 docs / skill docs に限る
- skill 本文の正本は引き続き `tools/codex-skills/` に置き、`conductor` を追加する場合も `tools/codex-skills/conductor/SKILL.md` を使う
- 特定 project の記事化用記録機構、tutorial 本文、validation の生ログは package の共通骨格へ含めない
- package 現行段階では runtime asset の同梱を先行し、generated repo への export と合わせて skill docs を段階導入してよい

## bounded multi-step と mirror gate
- package 側 `conductor` は same-block bounded multi-step を generic contract として同梱する
- `execution_level` は `MID` と `HIGH` の 2 段だけを許し、既定値は `MID`
- step 上限の既定値は `5` とし、human が明示した practical override だけを受ける
- `step=20` は bounded override の一例であり、無制限実行を意味しない
- `MID` は package 利用者向けの既定 level として読む
  - same-block bounded multi-step に加え、block-only 状態から次 block の chunk / ticket 生成へ進む narrow handoff までを含む
- `HIGH` はその `MID` を含んだ上位 level として読み、block close-ready 段階では `plan_manager` 返送を優先する
- reviewer handoff は direct dispatch target ではなく、bounded run 内の internal role として扱う
- machine-readable には `close_ready_handoff`, `high_cross_block_handoff`, `reviewer_pass_through` を載せ、wrapper note でも人間が読み分けられるようにする
- `.agents/skills/` mirror は package canonical source と package docs の validation 完了後に追随させる
- したがって設計上の順番は次で固定する
  - `tools/conductor/` と `tools/codex-skills/` を更新する
  - package docs だけで contract が閉じるか validation する
  - その後に generated repo と mirror へ反映する

## reference summary との分担
- この file は reference band の本体 docs として扱う
- `docs/references/design.md` は optional summary / hub として残してよい
- summary を残す場合も、canvas band の代替正本にはしない
- 本体には設計方針、入力、出力、抽象化境界、設計課題を残す
- summary には短い見取り図だけを置き、仕様全文は持ち込まない
