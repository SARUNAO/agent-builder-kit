# Codex Skills Inventory

このディレクトリには、現在同梱している skill と、まだ contract のみ先に定義している support skill を置く。

## 現在同梱している skill
- `plan-manager`
- `task-planner`
- `task-worker`
- `reviewer`
- `obsidian-canvas-sync`

## 置き場
- canonical source:
  - `tools/codex-skills/`
- user-facing export:
  - generated repo の `.agents/skills/`
- `.agents/skills/` が存在する generated repo では、利用者向け入口はそちらを優先してよい
- ただし正本管理は引き続き `tools/codex-skills/` で行う

## canonical 名
- canonical:
  - `plan-manager`
  - `task-planner`
  - `task-worker`
  - `reviewer`

## まだ同梱しない support skill
- `docs-sync`
  - 役割は summary docs と hub docs の整合補助
  - まだ contract のみで、`SKILL.md` は作成していない
  - 実装する場合は `obsidian_canvas pack` の asset として ship する
