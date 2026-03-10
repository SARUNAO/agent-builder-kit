---
name: task-planner
description: plan-spec を chunk と ticket へ分解する skill。chunks と tickets を更新し、親子関係と lane order を整えたうえで最後に obsidian-canvas-sync script を実行する。
---

# Task Planner

Use this skill when the user asks to break a plan into chunks and tickets, reorder work, or update execution structure beneath the plan layer.

## Read This First
- Read the project's `docs/OPERATIONAL_SCHEMA.md`.
- Read the project's `docs/ROLE_SKILLS.md`.
- Read the relevant `plan-spec`, `docs/exec-plans/blocks/*.md`, `docs/exec-plans/chunks/*.md`, and `docs/exec-plans/tickets/*.md`.
- If the repo uses Obsidian canvas, also read the `obsidian-canvas-sync` skill. The canonical source is `tools/codex-skills/obsidian-canvas-sync/SKILL.md`, and exported repos may expose `.agents/skills/obsidian-canvas-sync/SKILL.md`.

## You Own
- `docs/exec-plans/chunks/*.md`
- `docs/exec-plans/tickets/*.md`
- chunk 内 ticket table
- 例外的に、配下最初の chunk を `in_progress` に上げる瞬間だけ、親 block note の `pending -> in_progress` 同期を行ってよい

Do not change the human request or the plan goal. If the plan itself needs to change, hand the work back to `plan-manager`.

## Required Outcomes
1. Every chunk has a valid `parent_block`.
2. Every ticket has a valid `parent_chunk`.
3. Promote `ticket` to `done` only after reviewer sign-off and source docs sync have been checked.
4. `editable_paths`, `depends_on`, and `lane_order` are explicit enough for a worker to act.
5. 親 block の status 変更は、roll-up 整合のための `pending -> in_progress` 同期だけに限る。
6. `in_progress -> done`, `blocked`, `goal`, `depends_on`, `lane_order` など block の意味変更は `plan-manager` へ返す。
7. If chunk/ticket structure or status changed and Obsidian canvas is enabled, run canvas sync at the end.

## Sync Rule
- Run `obsidian-canvas-sync` only after updating docs/exec-plans/chunks/tickets.
- Prefer executing `scripts/sync_canvas.py` directly.
- If schema integrity is broken, fix the docs first and only then sync.
