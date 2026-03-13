---
name: obsidian-canvas-sync
description: Sync an Obsidian .canvas file from project planning docs by reading plan blocks, chunks, and tickets, then updating reserved A/B/C lanes while preserving manual notes outside the managed lanes.
---

# Obsidian Canvas Sync

Use this skill when a project uses Obsidian `.canvas` to visualize development flow progress and the user asks to create, refresh, or repair that canvas from planning docs.

This skill is also the terminal sync step for the role skills `plan-manager`, `task-planner`, and `task-worker`.

## Read This First
- Read the project's `docs/OBSIDIAN_CANVAS_SYNC.md`.
- Read the relevant `plan-spec`, `chunk-sheet`, and `ticket` docs.
- Use `scripts/sync_canvas.py` for actual JSON generation or update.
- Treat docs as source of truth. Do not infer missing IDs from prose when the structured fields are absent.

## Managed Model
- Lane A: high-level blocks from `plan-spec`
- Lane B: chunks from `chunk-sheet`
- Lane C: tickets from `ticket`
- Reference band: top-center primary docs for `Product Sense`, `Design`, `Human Manual`, and `Attention Queue`
- Optional summaries or hubs: `docs/references/*.md` when the project keeps them
- Preserve notes outside the managed lanes

## Required Structured Fields
- `block_id`
- `chunk_id`
- `parent_block`
- `ticket_id`
- `parent_chunk`

Prefer YAML frontmatter for these fields. Keep bullet metadata only as a fallback format.

Optional summary or hub notes use:
- `reference_id`
- `title`
- `lane_order`

If the project intentionally keeps those notes and these fields are missing, stop and ask for the source docs to be fixed first.

## Update Rules
1. Parse source docs.
2. Validate required IDs.
3. Run `scripts/sync_canvas.py`.
4. Review the updated `.canvas`.
5. Preserve or move manual notes outside managed lanes.
6. Treat primary docs as source of truth for the reference band; do not let optional summary or hub notes overrule them.

## Safety Rules
- Do not use `.canvas` as source of truth.
- Do not silently delete unknown nodes in managed lanes; move them to the manual lane when possible.
- Prefer deterministic regeneration of managed lanes over hand-editing JSON fragments.
- Do not treat generator code strings or legacy summary notes as higher priority than the docs contract.

## Script Usage
既定配置の repo では、引数なし実行を first choice とする。

```bash
python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py
```

override が必要なときだけ、明示引数を足す。

```bash
python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py \
  --plan-spec docs/exec-plans/plan-spec.md \
  --block-dir docs/exec-plans/blocks \
  --chunk-dir docs/exec-plans/chunks \
  --ticket-dir docs/exec-plans/tickets \
  --reference-dir docs/references \
  --vault-root path/to/vault-root \
  --canvas docs/exec-plans/canvas/development-flow.canvas
```

一部だけ explicit path を渡した場合でも、未指定の `block-dir`, `chunk-dir`, `ticket-dir`, `reference-dir`, `canvas` は同じ repo / fixture root から補完される前提で読む。current workspace 側の default path を混ぜない。

`.agents/skills/` が存在しない repo では、同じ script を `tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py` から実行してよい。

```bash
python3 tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py
```

```bash
python3 tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py \
  --plan-spec docs/exec-plans/plan-spec.md \
  --block-dir docs/exec-plans/blocks \
  --chunk-dir docs/exec-plans/chunks \
  --ticket-dir docs/exec-plans/tickets \
  --reference-dir docs/references \
  --vault-root path/to/vault-root \
  --canvas docs/exec-plans/canvas/development-flow.canvas
```
