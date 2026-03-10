# Agent Hub

このリポジトリの Agent 指示はこのファイルを正とする。

## Scope
- このプロジェクトの目的は `mdBook Workshop` を進めるための docs 駆動フローを運用すること。
- 正本 docs は `docs/` に置く。
- planning source は `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks`, `docs/exec-plans/chunks`, `docs/exec-plans/tickets` を使う。
- skill asset の canonical source は `tools/codex-skills/` に置く。
- `.agents/skills/` が存在する場合、それは利用者向け export 層として扱い、正本は引き続き `tools/codex-skills/` とする。

## Bootstrap
1. `docs/index.md` を読む。
2. `docs/PLANS.md` を読む。
3. `docs/exec-plans/active/attention-queue.md` を読む。
4. `docs/exec-plans/completed/progress-log.md` を読む。
5. `docs/PRODUCT_SENSE.md` と `docs/DESIGN.md` を読む。

## Roles
- `Human operator`: 優先順位、採否判断、抽象化レベルの裁定を行う。
- `プランオーナー`: 上流判断と plan 更新を行う。
- `タスクプランナー`: `plan` を `chunk` と `ticket` へ分解する。
- `タスクワーカー`: ticket の範囲だけを実装し、事実を返す。
- `reviewer`: code ticket の後段 review を行い、docs-only ticket では skip できる。

## Routing
- 入口: `docs/index.md`
- 価値仮説: `docs/PRODUCT_SENSE.md`
- 設計: `docs/DESIGN.md`
- 運用 schema: `docs/OPERATIONAL_SCHEMA.md`
- role skill: `docs/ROLE_SKILLS.md`

## Skill Routing
- source repo では `tools/codex-skills/` を canonical source として読む。
- `.agents/skills/` が存在する場合、利用者向けの入口は `.agents/skills/` を優先してよい。
- ただし `.agents/skills/` は export 層であり、skill 本文の正本管理先ではない。
