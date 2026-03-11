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
  - 役割は optional summary docs と hub docs の整合補助
  - まだ contract のみで、`SKILL.md` は作成していない
  - 実装する場合は `obsidian_canvas pack` の asset として ship する

## current contract
- reference band は `direct-source` を前提とし、`Product Sense`, `Design`, `Human Manual`, `Attention Queue` の本体 docs を一次入力として扱う
- `docs/references/*.md` は残す場合も optional summary / hub として扱い、本体 docs の代替正本にはしない
- generated attention queue の static seed は docs 正本を前提とし、`AI案内可 / 条件付き / 人間判断必須` の境界を保つ
