# Acceptance Matrix

release 前に最低限確認する profile / pack ごとの受け入れ基準。

## 基本方針
- まず `standard + obsidian_canvas_pack` を通す
- その後 `migration_pack` と `self_hosting_pack` を追加確認する
- source repo だけでなく `agent-builder-kit` 単体展開でも破綻しないことを重視する

## Matrix

| scenario | command | 必須確認 | 備考 |
|---|---|---|---|
| `standard + obsidian_canvas_pack` | `python3 tests/test_clean_workspace_smoke.py` | `docs/exec-plans/plan-spec.md`, `docs/references/`, `tools/codex-skills/`, `.agents/skills/`, generated `AGENTS.md` / `README.md` | 基本受け入れ。最初に回す |
| source / package / generated 整合 | `python3 tests/test_validation_checks.py` | skill bundle 3 面一致、主要 relative link、`block_id` / `chunk_id` / `ticket_id` 重複なし | stale note や mirror 漏れの検知 |
| `migration_pack + obsidian_canvas_pack` | `python3 tests/test_profile_pack_smoke.py` | `MIGRATION_START_HERE.md`, `docs/migration/index.md`, `project-inventory.md`, `gap-report.md`, `adoption-plan.md`, `current-ai-migration-request.md` | self-hosting docs は不要 |
| `self_hosting_pack + obsidian_canvas_pack` | `python3 tests/test_profile_pack_smoke.py` | `docs/INPUT_SCHEMA.md`, `docs/OUTPUT_PROFILES.md`, `docs/DOCS_BUILDER_TOML.md`, `docs/INIT_RUNNER.md`, `docs/RENDERING_RULES.md` | `agent-builder-kit` 単体展開でも fallback で成功すること |
| package docs walkthrough | `README.md`, `docs/index.md`, `docs/HUMAN_MANUAL.md` を目視 | package 単体の入口、role 導線、release gate の読みやすさ | 人間が release 前に見る手順 |

## Release Gate

次に進めてよい条件は以下。

- `python3 tests/test_clean_workspace_smoke.py` が通る
- `python3 tests/test_validation_checks.py` が通る
- `python3 tests/test_profile_pack_smoke.py` が通る
- package README / docs hub / Human Manual の導線を読み合わせ済み
- current docs の入口が揃っている
  - [index.md](./index.md)
  - [INIT_RUNNER.md](./INIT_RUNNER.md)
  - [OUTPUT_PROFILES.md](./OUTPUT_PROFILES.md)
  - [ROLE_SKILLS.md](./ROLE_SKILLS.md)

## よくある見落とし
- `tools/codex-skills/` だけ更新して `.agents/skills/` mirror を見ない
- generated repo の profile 差分を見ずに、存在しない doc を欠落扱いする
- `agent-builder-kit` 単体展開でしか起きない fallback 不備を見逃す
- docs hub の相対リンクは直したが package mirror を追従しない
