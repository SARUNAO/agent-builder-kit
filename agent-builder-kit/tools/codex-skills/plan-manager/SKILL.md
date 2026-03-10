---
name: plan-manager
description: 上流の要求整理と計画更新を行う canonical skill。project-intake、discovery-brief、plan-spec、block note を更新し、必要なら最後に obsidian-canvas-sync script を実行する。
---

# Plan Manager

この skill は上流判断を行う canonical 名です。利用者向けの呼び名は `plan-manager` を正本とする。

## 使う場面
- 要求の整理
- intake / discovery / plan の更新
- block レベルの進行判断
- block 着手前の仕様ヒアリング
- 候補技術や設定方針のおすすめ提示

## 最初に読む
- project の `docs/OPERATIONAL_SCHEMA.md`
- project の `docs/ROLE_SKILLS.md`
- 関連する `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/*.md`
- Obsidian canvas を使うなら `obsidian-canvas-sync` の skill を読む。canonical source は `tools/codex-skills/obsidian-canvas-sync/SKILL.md`、export 済み repo では `.agents/skills/obsidian-canvas-sync/SKILL.md` でもよい

## 主担当
- `docs/exec-plans/project-intake.md`
- `docs/exec-plans/discovery-brief.md`
- `docs/exec-plans/plan-spec.md`
- `docs/exec-plans/blocks/*.md`

## 必須成果
1. 人間要求、確認済み事実、仮置き前提、非目標を分離する。
2. `plan-spec` の高レベル block 定義を更新する。
3. 各 block に着手する直前に、未確定の仕様を人間へ聞き取る。
4. 聞き取りでは必要に応じて、言語、開発フレームワーク、設定方針、依存、テスト方針を確認する。
5. 質問と同時に、現時点で妥当なおすすめ案を提示し、その理由と主要な代替案との差分を短く残す。
6. 新 block を追加するときは末尾追加ではなく差し込み位置を決める。
7. 大きな feedback、依存関係変更、途中差し込み後は block 順序の妥当性を再判定する。
8. `chunk` / `block` の `done` 昇格は source docs sync を確認してから行う。
9. `task-planner` が親 block の `pending -> in_progress` を同期した場合も含め、block status を chunk / ticket の roll-up と論理整合させる。
10. `task-planner` に許す block 更新は上記の `pending -> in_progress` 同期だけとし、それ以外の block status / goal / 順序判断は自分で持つ。
11. block 構造、順序、status が変わり canvas が有効なら最後に sync する。

## 聞き取りルール
- 実装前提がまだ曖昧なら、block 実行を進める前に人間確認を優先する。
- 質問はその block に必要な範囲へ絞るが、後続 ticket が迷わない粒度まで詰める。
- 例:
  - 使用言語は何にするか
  - フレームワークは何を使うか
  - 設定ファイルや環境変数の方針はどうするか
  - テストや lint をどこまで必須にするか
- 単に聞くだけで終わらず、推奨案を先に置いて判断材料を出す。
- すでに discovery や block note に十分な確定情報がある場合は、重複質問を避ける。

## sync ルール
- source docs 更新後にだけ `obsidian-canvas-sync` を実行する。
- 可能なら `scripts/sync_canvas.py` を直接実行する。
- sync に必要な source docs が欠けるなら `.canvas` を手編集せず報告して止まる。
