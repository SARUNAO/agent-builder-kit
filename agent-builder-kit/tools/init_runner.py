#!/usr/bin/env python3
"""Bootstrap a new workflow docs skeleton from docs-builder.toml."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    tomllib = None


ROOT = Path(__file__).resolve().parent.parent
BUILDER_DOCS = ROOT / "docs"
PLANNING_TEMPLATES = BUILDER_DOCS / "templates"
WORKFLOW_REFERENCES = BUILDER_DOCS / "references"
SKILLS_ROOT = ROOT / "tools" / "codex-skills"

DEFAULT_REFERENCE_SEED = ["product_sense", "design", "attention_queue", "human_manual"]
REFERENCE_SEED_MAP = {
    "product_sense": ("REF-PRODUCT-SENSE", "Product Sense", "このプロジェクトの目的、価値、対象ユーザーを置く。"),
    "design": ("REF-DESIGN", "Design", "設計上の前提、制約、構成判断を置く。"),
    "attention_queue": ("REF-ATTENTION", "Attention Queue", "後で再注目する事項を置く。"),
    "human_manual": ("REF-HUMAN-MANUAL", "Human Manual", "人間向けの運用メモと判断ルールを置く。"),
}


@dataclass
class Config:
    manifest_path: Path
    output_root: Path
    planning_root: Path
    active_dir: Path
    completed_dir: Path
    completed_entries_dir: Path
    overwrite: bool
    schema_version: int
    project_name: str
    project_slug: str
    project_mode: str
    project_request: str
    project_summary: str
    primary_deliverable: str
    role_model: str
    profile: str
    packs: list[str]
    self_hosting_enabled: bool
    review_required: bool
    discovery_confirmed: list[str]
    discovery_assumptions: list[str]
    discovery_non_goals: list[str]
    discovery_constraints: list[str]
    migration_enabled: bool
    migration_current_state: str
    migration_adoption_goal: str
    migration_existing_docs: list[str]
    migration_known_gaps: list[str]
    migration_protected_paths: list[str]
    migration_notes: list[str]
    seed_discovery_block: bool
    reference_seed: list[str]
    canvas_enabled: bool
    canvas_path: Path
    reference_dir: Path
    vault_root: Path
    intake_path: Path
    discovery_path: Path
    plan_spec_path: Path
    blocks_dir: Path
    chunks_dir: Path
    tickets_dir: Path
    fact_reports_dir: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a workflow docs skeleton from docs-builder.toml.")
    parser.add_argument("manifest", nargs="?", default="docs-builder.toml", help="Path to docs-builder.toml")
    parser.add_argument("--output-root", help="Override generation.output_root")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files even in safe_merge mode")
    parser.add_argument(
        "--cleanup-package",
        action="store_true",
        help="Delete the local agent-builder-kit directory after a successful bootstrap when running from agent-builder-kit/tools/init_runner.py",
    )
    return parser.parse_args()


def load_config(args: argparse.Namespace) -> Config:
    manifest_path = Path(args.manifest).resolve()
    data = load_toml(manifest_path.read_text(encoding="utf-8"))

    project = data["project"]
    workflow = data["workflow"]
    discovery = data.get("discovery", {})
    migration = data.get("migration", {})
    generation = data.get("generation", {})
    bootstrap = data.get("bootstrap", {})
    obsidian = data.get("obsidian", {})

    output_root = Path(args.output_root or generation.get("output_root", ".")).expanduser()
    if not output_root.is_absolute():
        output_root = (manifest_path.parent / output_root).resolve()

    planning_root_value = generation.get("planning_root", "docs/exec-plans")
    planning_root = Path(planning_root_value).expanduser()
    if not planning_root.is_absolute():
        planning_root = (output_root / planning_root).resolve()
    active_dir = planning_root / "active"
    completed_dir = planning_root / "completed"
    completed_entries_dir = completed_dir / "entries"

    overwrite_policy = generation.get("overwrite_policy", "safe_merge")
    overwrite = args.force or overwrite_policy == "replace_generated_only"

    packs = list(workflow.get("packs", []))
    canvas_enabled = "obsidian_canvas_pack" in packs
    migration_enabled = project["mode"] == "migration" or "migration_pack" in packs
    self_hosting_enabled = "self_hosting_pack" in packs
    reference_dir = resolve_runtime_path(
        obsidian.get("reference_dir"),
        output_root=output_root,
        default_path=output_root / "docs" / "references",
    )
    canvas_path = resolve_runtime_path(
        obsidian.get("canvas_path"),
        output_root=output_root,
        default_path=planning_root / "canvas" / "development-flow.canvas",
    )

    intake_path = planning_root / "project-intake.md"
    discovery_path = planning_root / "discovery-brief.md"
    plan_spec_path = planning_root / "plan-spec.md"
    blocks_dir = planning_root / "blocks"
    chunks_dir = planning_root / "chunks"
    tickets_dir = planning_root / "tickets"
    fact_reports_dir = planning_root / "fact-reports"

    return Config(
        manifest_path=manifest_path,
        output_root=output_root,
        planning_root=planning_root,
        active_dir=active_dir,
        completed_dir=completed_dir,
        completed_entries_dir=completed_entries_dir,
        overwrite=overwrite,
        schema_version=int(data.get("schema_version", 1)),
        project_name=project["name"],
        project_slug=project["slug"],
        project_mode=project["mode"],
        project_request=project["request"],
        project_summary=project.get("summary", ""),
        primary_deliverable=project.get("primary_deliverable", ""),
        role_model=workflow["role_model"],
        profile=workflow["profile"],
        packs=packs,
        self_hosting_enabled=self_hosting_enabled,
        review_required=bool(workflow.get("review_required", True)),
        discovery_confirmed=list(discovery.get("confirmed", [])),
        discovery_assumptions=list(discovery.get("assumptions", [])),
        discovery_non_goals=list(discovery.get("non_goals", [])),
        discovery_constraints=list(discovery.get("constraints", [])),
        migration_enabled=migration_enabled,
        migration_current_state=migration.get("current_state", "現行運用の把握が未完了"),
        migration_adoption_goal=migration.get("adoption_goal", "既存運用を新 schema へ安全に移行する"),
        migration_existing_docs=list(migration.get("existing_docs", [])),
        migration_known_gaps=list(migration.get("known_gaps", [])),
        migration_protected_paths=list(migration.get("protected_paths", [])),
        migration_notes=list(migration.get("notes", [])),
        seed_discovery_block=bool(bootstrap.get("seed_discovery_block", True)),
        reference_seed=list(bootstrap.get("reference_seed", DEFAULT_REFERENCE_SEED)),
        canvas_enabled=canvas_enabled,
        canvas_path=canvas_path,
        reference_dir=reference_dir,
        vault_root=output_root,
        intake_path=intake_path,
        discovery_path=discovery_path,
        plan_spec_path=plan_spec_path,
        blocks_dir=blocks_dir,
        chunks_dir=chunks_dir,
        tickets_dir=tickets_dir,
        fact_reports_dir=fact_reports_dir,
    )


def resolve_runtime_path(raw_value: str | None, output_root: Path, default_path: Path) -> Path:
    if raw_value is None:
        return default_path
    path = Path(raw_value).expanduser()
    if path.is_absolute():
        return path
    return (output_root / path).resolve()


def load_toml(text: str) -> dict:
    if tomllib is not None:
        return tomllib.loads(text)
    return parse_simple_toml(text)


def parse_simple_toml(text: str) -> dict:
    data: dict[str, object] = {}
    current = data
    pending_key: str | None = None
    pending_lines: list[str] = []

    for raw_line in text.splitlines():
        line = strip_comment(raw_line).strip()
        if not line:
            continue

        if pending_key is not None:
            pending_lines.append(line)
            joined = " ".join(pending_lines)
            if is_balanced_array(joined):
                current[pending_key] = parse_toml_value(joined)
                pending_key = None
                pending_lines = []
            continue

        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].strip()
            current = data.setdefault(section_name, {})
            if not isinstance(current, dict):
                raise ValueError(f"TOML section conflict: {section_name}")
            continue

        if "=" not in line:
            raise ValueError(f"Unsupported TOML line: {line}")
        key, value = [part.strip() for part in line.split("=", 1)]
        if value.startswith("[") and not is_balanced_array(value):
            pending_key = key
            pending_lines = [value]
            continue
        current[key] = parse_toml_value(value)

    if pending_key is not None:
        raise ValueError(f"Unclosed TOML array for key: {pending_key}")
    return data


def strip_comment(line: str) -> str:
    in_quote = False
    escaped = False
    out: list[str] = []
    for char in line:
        if char == '"' and not escaped:
            in_quote = not in_quote
        if char == "#" and not in_quote:
            break
        out.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(out)


def is_balanced_array(value: str) -> bool:
    depth = 0
    in_quote = False
    escaped = False
    for char in value:
        if char == '"' and not escaped:
            in_quote = not in_quote
        elif not in_quote:
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return depth == 0


def parse_toml_value(value: str):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_toml_value(part.strip()) for part in split_array_items(inner)]
    try:
        return int(value)
    except ValueError:
        return value


def split_array_items(text: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    in_quote = False
    escaped = False
    for char in text:
        if char == '"' and not escaped:
            in_quote = not in_quote
        if char == "," and not in_quote:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
            continue
        current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    item = "".join(current).strip()
    if item:
        items.append(item)
    return items


def main() -> int:
    args = parse_args()
    config = load_config(args)

    generated: list[str] = []
    copied: list[str] = []

    ensure_dirs(config)
    generated.extend(generate_core_docs(config))
    copied.extend(copy_references(config))
    copied.extend(copy_skills(config))
    copied.extend(copy_templates(config))
    copied.extend(copy_self_hosting_assets(config))
    generated.extend(generate_runtime_seed(config))
    if config.canvas_enabled:
        generated.extend(generate_canvas(config))
    cleanup_result = cleanup_source_package(args, config)

    print(
        json.dumps(
            {
                "status": "ok",
                "output_root": str(config.output_root),
                "generated_files": len(generated),
                "copied_files": len(copied),
                "canvas_enabled": config.canvas_enabled,
                "profile": config.profile,
                **cleanup_result,
            },
            ensure_ascii=False,
        )
    )
    return 0


def cleanup_source_package(args: argparse.Namespace, config: Config) -> dict[str, str]:
    if not args.cleanup_package:
        return {"package_cleanup": "kept_by_default"}
    if ROOT.name != "agent-builder-kit":
        return {"package_cleanup": "skipped", "package_cleanup_reason": "not_running_from_agent_builder_kit"}
    if not ROOT.exists():
        return {"package_cleanup": "skipped", "package_cleanup_reason": "package_root_missing"}
    if ROOT == config.output_root or ROOT in config.output_root.parents:
        return {"package_cleanup": "skipped", "package_cleanup_reason": "output_root_inside_agent_builder_kit"}
    shutil.rmtree(ROOT)
    return {"package_cleanup": "removed", "package_cleanup_target": str(ROOT)}


def ensure_dirs(config: Config) -> None:
    dirs = [
        config.output_root,
        config.output_root / ".agents",
        config.output_root / ".agents" / "skills",
        config.output_root / "docs",
        config.output_root / "docs" / "references",
        config.output_root / "tools",
        config.output_root / "tools" / "codex-skills",
        config.planning_root,
        config.active_dir,
        config.completed_dir,
        config.blocks_dir,
        config.chunks_dir,
        config.tickets_dir,
        config.fact_reports_dir,
    ]
    if config.profile in {"standard", "expanded"}:
        dirs.append(config.output_root / "docs" / "templates")
    if config.migration_enabled:
        dirs.append(config.output_root / "docs" / "migration")
    if config.canvas_enabled:
        dirs.append(config.reference_dir)
        dirs.append(config.canvas_path.parent)
    for path in dirs:
        path.mkdir(parents=True, exist_ok=True)


def generate_core_docs(config: Config) -> list[str]:
    files: dict[Path, str] = {
        config.output_root / "AGENTS.md": render_agents(config),
        config.output_root / "README.md": render_root_readme(config),
        config.output_root / "docs" / "index.md": render_docs_index(config),
        config.output_root / "docs" / "PLANS.md": render_plans(),
        config.output_root / "docs" / "PRODUCT_SENSE.md": render_product_sense(config),
        config.output_root / "docs" / "DESIGN.md": render_design(config),
        config.output_root / "docs" / "HUMAN_MANUAL.md": render_human_manual(config),
        config.active_dir / "index.md": "# Active Plans\n\n- [attention-queue.md](./attention-queue.md)\n",
        config.active_dir / "attention-queue.md": render_attention_queue(),
        config.completed_dir / "index.md": "# Completed Logs\n\n- [progress-log.md](./progress-log.md)\n- [ENTRY_TEMPLATE.md](./ENTRY_TEMPLATE.md)\n",
        config.completed_dir / "progress-log.md": "# 進捗ダイジェスト\n\n## 直近の完了\n- まだなし\n",
        config.completed_dir / "ENTRY_TEMPLATE.md": BUILDER_DOCS.joinpath("exec-plans/completed/ENTRY_TEMPLATE.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "references" / "index.md": "# References\n\n- [roles.md](./roles.md)\n- [lifecycle.md](./lifecycle.md)\n- [review-policy.md](./review-policy.md)\n",
    }
    if config.profile in {"minimum", "standard", "expanded"}:
        files[config.output_root / "docs" / "OPERATIONAL_SCHEMA.md"] = BUILDER_DOCS.joinpath("OPERATIONAL_SCHEMA.md").read_text(encoding="utf-8")
        files[config.output_root / "docs" / "ROLE_SKILLS.md"] = BUILDER_DOCS.joinpath("ROLE_SKILLS.md").read_text(encoding="utf-8")
    if config.canvas_enabled:
        files[config.output_root / "docs" / "OBSIDIAN_CANVAS_SYNC.md"] = BUILDER_DOCS.joinpath("OBSIDIAN_CANVAS_SYNC.md").read_text(encoding="utf-8")
    if config.migration_enabled:
        files[config.output_root / "MIGRATION_START_HERE.md"] = render_migration_start_here()
    if config.self_hosting_enabled:
        files.update(render_self_hosting_overrides(config))

    written: list[str] = []
    managed_seed_sources = build_managed_seed_sources(config)
    for path, content in files.items():
        if write_text(path, content, config.overwrite, replace_if_matches=managed_seed_sources.get(path)):
            written.append(str(path))
    return written


def copy_references(config: Config) -> list[str]:
    if config.self_hosting_enabled:
        return []
    copied: list[str] = []
    for name in ["roles.md", "lifecycle.md", "review-policy.md"]:
        src = WORKFLOW_REFERENCES / name
        dst = config.output_root / "docs" / "references" / name
        if copy_file(src, dst, config.overwrite):
            copied.append(str(dst))
    return copied


def copy_skills(config: Config) -> list[str]:
    copied: list[str] = []
    skills = [
        "plan-manager",
        "task-planner",
        "task-worker",
        "reviewer",
        "obsidian-canvas-sync",
    ]
    inventory_src = SKILLS_ROOT / "README.md"
    inventory_targets = [
        config.output_root / "tools" / "codex-skills" / "README.md",
        config.output_root / ".agents" / "skills" / "README.md",
    ]
    for inventory_dst in inventory_targets:
        if copy_file(inventory_src, inventory_dst, config.overwrite):
            copied.append(str(inventory_dst))
    for skill in skills:
        src = SKILLS_ROOT / skill
        destinations = [
            config.output_root / "tools" / "codex-skills" / skill,
            config.output_root / ".agents" / "skills" / skill,
        ]
        for dst in destinations:
            if copy_tree(src, dst, config.overwrite):
                copied.append(str(dst))
    return copied


def copy_templates(config: Config) -> list[str]:
    if config.profile not in {"standard", "expanded"}:
        return []
    template_names = [
        "project-intake-template.md",
        "discovery-brief-template.md",
        "plan-spec-template.md",
        "chunk-sheet-template.md",
        "ticket-template.md",
        "fact-report-template.md",
        "chunk-close-template.md",
    ]
    if config.canvas_enabled:
        template_names.append("block-note-template.md")
    if config.migration_enabled:
        template_names.extend(
            [
                "project-inventory-template.md",
                "gap-report-template.md",
                "adoption-plan-template.md",
                "current-ai-migration-request-template.md",
            ]
        )
    copied: list[str] = []
    for name in template_names:
        src = PLANNING_TEMPLATES / name
        dst = config.output_root / "docs" / "templates" / name
        if copy_file(src, dst, config.overwrite):
            copied.append(str(dst))
    return copied


def copy_self_hosting_assets(config: Config) -> list[str]:
    if not config.self_hosting_enabled:
        return []
    copied: list[str] = []
    trees = [
        (BUILDER_DOCS / "references", config.output_root / "docs" / "references"),
        (BUILDER_DOCS / "exec-plans" / "completed" / "entries", config.completed_entries_dir),
    ]
    for src, dst in trees:
        if src.exists() and copy_tree(src, dst, config.overwrite):
            copied.append(str(dst))
    return copied


def generate_runtime_seed(config: Config) -> list[str]:
    today = date.today().isoformat()
    plan_id = f"PLAN-{today}-{config.project_slug.upper().replace('-', '-')}"
    project_files: dict[Path, str] = {
        config.intake_path: render_project_intake(config, plan_id, today),
        config.discovery_path: render_discovery_brief(config, plan_id, today),
        config.plan_spec_path: render_plan_spec(config, plan_id, today),
    }
    if config.seed_discovery_block:
        block_name = "block-001-migration-inventory.md" if config.migration_enabled else "block-001-discovery.md"
        project_files[config.blocks_dir / block_name] = render_seed_block(config, plan_id)
    if config.migration_enabled:
        project_files.update(
            {
                config.output_root / "docs" / "migration" / "index.md": render_migration_index(),
                config.output_root / "docs" / "migration" / "project-inventory.md": render_project_inventory(config, plan_id, today),
                config.output_root / "docs" / "migration" / "gap-report.md": render_gap_report(config, plan_id, today),
                config.output_root / "docs" / "migration" / "adoption-plan.md": render_adoption_plan(config, plan_id, today),
                config.output_root / "docs" / "migration" / "current-ai-migration-request.md": render_current_ai_migration_request(config, plan_id, today),
            }
        )
    for ref_name in config.reference_seed:
        ref_note = render_reference_seed(ref_name)
        if ref_note is None:
            continue
        filename, content = ref_note
        project_files[config.reference_dir / filename] = content

    written: list[str] = []
    for path, content in project_files.items():
        if write_text(path, content, config.overwrite):
            written.append(str(path))
    return written


def generate_canvas(config: Config) -> list[str]:
    sync_script = config.output_root / "tools" / "codex-skills" / "obsidian-canvas-sync" / "scripts" / "sync_canvas.py"
    cmd = [
        sys.executable,
        str(sync_script),
        "--plan-spec",
        str(config.plan_spec_path),
        "--block-dir",
        str(config.blocks_dir),
        "--chunk-dir",
        str(config.chunks_dir),
        "--ticket-dir",
        str(config.tickets_dir),
        "--reference-dir",
        str(config.reference_dir),
        "--vault-root",
        str(config.vault_root),
        "--canvas",
        str(config.canvas_path),
    ]
    subprocess.run(cmd, check=True, cwd=config.output_root)
    return [str(config.canvas_path)]


def write_text(
    path: Path,
    content: str,
    overwrite: bool,
    replace_if_matches: list[str] | None = None,
) -> bool:
    if path.exists() and not overwrite:
        existing = path.read_text(encoding="utf-8")
        allowed = replace_if_matches or []
        normalized_existing = existing.rstrip() + "\n"
        normalized_allowed = {item.rstrip() + "\n" for item in allowed}
        if normalized_existing not in normalized_allowed:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def copy_file(src: Path, dst: Path, overwrite: bool) -> bool:
    if dst.exists() and not overwrite:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_tree(src: Path, dst: Path, overwrite: bool) -> bool:
    if dst.exists():
        if not overwrite:
            return False
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return True


def render_agents(config: Config) -> str:
    role_owner = "プランオーナー" if config.role_model == "four_role_default" else "プランマネージャー / 仕様設計者"
    intake_path = format_relative_path(config.output_root, config.intake_path)
    discovery_path = format_relative_path(config.output_root, config.discovery_path)
    plan_spec_path = format_relative_path(config.output_root, config.plan_spec_path)
    blocks_dir = format_relative_path(config.output_root, config.blocks_dir)
    chunks_dir = format_relative_path(config.output_root, config.chunks_dir)
    tickets_dir = format_relative_path(config.output_root, config.tickets_dir)
    return textwrap.dedent(
        f"""
        # Agent Hub

        このリポジトリの Agent 指示はこのファイルを正とする。

        ## Scope
        - このプロジェクトの目的は `{config.project_name}` を進めるための docs 駆動フローを運用すること。
        - 正本 docs は `docs/` に置く。
        - planning source は `{intake_path}`, `{discovery_path}`, `{plan_spec_path}`, `{blocks_dir}`, `{chunks_dir}`, `{tickets_dir}` を使う。
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
        - `{role_owner}`: 上流判断と plan 更新を行う。
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
        """
    ).strip()


def render_root_readme(config: Config) -> str:
    plan_spec_path = format_relative_path(config.output_root, config.plan_spec_path)
    blocks_dir = format_relative_path(config.output_root, config.blocks_dir)
    canvas_path = format_relative_path(config.output_root, config.canvas_path) if config.canvas_enabled else "未生成"
    lines = [
        f"# {config.project_name}",
        "",
        "AI コーディング前提の開発フローを運用するための docs 駆動 workspace。",
        "",
        "## 最初に理解しておくこと",
        "- init 後に `agent-builder-kit/` を削除した場合、展開元 package の docs や相対パスはもう前提にしない",
        "- Codex アプリを再起動して project を開き直したあとの AI は、bootstrap 前や直前セッションの文脈を持っていない前提で扱う",
        "- そのため、この repo の作業は毎回 `AGENTS.md` と `docs/` を読み直すところから始める",
        "",
        "## Codex アプリでの再開手順",
        "1. いまのスレッドを閉じる",
        "2. Skill の反映同期のため、Codex アプリを再起動する",
        "3. この project を新しい project として開き直す",
        "4. 新しいセッションの AI に、まず `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HUMAN_MANUAL.md` を読むよう依頼する",
        "5. その後で `plan-manager` から作業を始める",
        "",
        "## 入口",
        "- `AGENTS.md`",
        "- `docs/index.md`",
        "- `docs/HUMAN_MANUAL.md`",
        "- `docs/PLANS.md`",
    ]
    if config.profile in {"minimum", "standard", "expanded"}:
        lines.append("- `docs/ROLE_SKILLS.md`")
    if config.self_hosting_enabled:
        lines.extend(
            [
                "",
                "## builder meta docs",
                "- `docs/INIT_RUNNER.md`",
                "- `docs/DOCS_BUILDER_TOML.md`",
            ]
        )
    lines.extend(
        [
            "",
            "## runtime artefact",
            f"- planning: `{plan_spec_path}`, `{blocks_dir}`",
            f"- canvas: `{canvas_path}`",
            "- canonical skill source: `tools/codex-skills/`",
            "- user-facing skill export: `.agents/skills/`",
            "",
            "## 進め方",
            "- `plan-manager` に目的と追加要件を伝える",
            "- `task-planner` に chunk / ticket を切ってもらう",
            "- `task-worker` と `reviewer` で実装と確認を進める",
        ]
    )
    return "\n".join(lines)


def render_docs_index(config: Config) -> str:
    core = [
        "- [PLANS.md](./PLANS.md)",
        "- [PRODUCT_SENSE.md](./PRODUCT_SENSE.md)",
        "- [DESIGN.md](./DESIGN.md)",
        "- [HUMAN_MANUAL.md](./HUMAN_MANUAL.md)",
    ]
    if config.profile in {"minimum", "standard", "expanded"}:
        core.extend(
            [
                "- [OPERATIONAL_SCHEMA.md](./OPERATIONAL_SCHEMA.md)",
                "- [ROLE_SKILLS.md](./ROLE_SKILLS.md)",
            ]
        )
    if config.canvas_enabled:
        core.append("- [OBSIDIAN_CANVAS_SYNC.md](./OBSIDIAN_CANVAS_SYNC.md)")
    lines = [
        "# Docs Hub",
        "",
        "## Core",
        *core,
        "",
        "## Execution",
        "- [exec-plans/active/index.md](./exec-plans/active/index.md)",
        "- [exec-plans/active/attention-queue.md](./exec-plans/active/attention-queue.md)",
        "- [exec-plans/completed/progress-log.md](./exec-plans/completed/progress-log.md)",
    ]
    if config.migration_enabled:
        lines.extend(
            [
                "",
                "## Migration",
                "- [migration/index.md](./migration/index.md)",
            ]
        )
    lines.extend(
        [
            "",
            "## References",
            "- [references/index.md](./references/index.md)",
        ]
    )
    return "\n".join(lines)


def render_self_hosting_overrides(config: Config) -> dict[Path, str]:
    agents_source = ROOT / "AGENTS.md"
    readme_source = ROOT / "README.md"
    files = {
        config.output_root / "AGENTS.md": (
            agents_source.read_text(encoding="utf-8") if agents_source.exists() else render_agents(config)
        ),
        config.output_root / "README.md": render_root_readme(config),
        config.output_root / "docs" / "index.md": BUILDER_DOCS.joinpath("index.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "PRODUCT_SENSE.md": BUILDER_DOCS.joinpath("PRODUCT_SENSE.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "DESIGN.md": BUILDER_DOCS.joinpath("DESIGN.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "PLANS.md": BUILDER_DOCS.joinpath("PLANS.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "INPUT_SCHEMA.md": BUILDER_DOCS.joinpath("INPUT_SCHEMA.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "OUTPUT_PROFILES.md": BUILDER_DOCS.joinpath("OUTPUT_PROFILES.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "DOCS_BUILDER_TOML.md": BUILDER_DOCS.joinpath("DOCS_BUILDER_TOML.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "INIT_RUNNER.md": BUILDER_DOCS.joinpath("INIT_RUNNER.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "RENDERING_RULES.md": BUILDER_DOCS.joinpath("RENDERING_RULES.md").read_text(encoding="utf-8"),
        config.output_root / "docs" / "HUMAN_MANUAL.md": BUILDER_DOCS.joinpath("HUMAN_MANUAL.md").read_text(encoding="utf-8"),
        config.active_dir / "index.md": BUILDER_DOCS.joinpath("exec-plans/active/index.md").read_text(encoding="utf-8"),
        config.active_dir / "attention-queue.md": BUILDER_DOCS.joinpath("exec-plans/active/attention-queue.md").read_text(encoding="utf-8"),
        config.completed_dir / "index.md": BUILDER_DOCS.joinpath("exec-plans/completed/index.md").read_text(encoding="utf-8"),
        config.completed_dir / "progress-log.md": BUILDER_DOCS.joinpath("exec-plans/completed/progress-log.md").read_text(encoding="utf-8"),
    }
    builder_foundation = BUILDER_DOCS / "exec-plans" / "active" / "builder-foundation.md"
    if builder_foundation.exists():
        files[config.active_dir / "builder-foundation.md"] = builder_foundation.read_text(
            encoding="utf-8"
        )
    return files


def render_plans() -> str:
    return textwrap.dedent(
        """
        # Plans

        ## 今日の入口
        1. `exec-plans/active/attention-queue.md`
        2. `exec-plans/completed/progress-log.md`

        ## Active Plans
        - まだなし

        ## 今の狙い
        - 要求を仕様化し、block / chunk / ticket の流れを回せるようにする
        - docs と review の粒度を固定する

        ## 直近の未確定事項
        - まだなし
        """
    ).strip()


def render_product_sense(config: Config) -> str:
    summary = config.project_summary or "まだ整理中"
    deliverable = config.primary_deliverable or "未確定"
    return textwrap.dedent(
        f"""
        # Product Sense

        ## このプロジェクトは何か
        - {summary}

        ## 人間要求
        - {config.project_request}

        ## 想定成果物
        - {deliverable}

        ## 非目的
        - 実装前に確定する
        """
    ).strip()


def render_design(config: Config) -> str:
    packs = ", ".join(config.packs) if config.packs else "なし"
    seed_title = "現行運用を棚卸しする" if config.migration_enabled else "何を作るか決める"
    seed_action = (
        "現行 docs と運用を棚卸しし、migration docs と写像方針を作る"
        if config.migration_enabled
        else "`プランオーナー` が聞き取りを通じて block を増やしていく"
    )
    return textwrap.dedent(
        f"""
        # Design

        ## 前提
        - project mode: `{config.project_mode}`
        - profile: `{config.profile}`
        - role model: `{config.role_model}`
        - packs: {packs}

        ## 生成方針
        - docs を source of truth とする
        - role skill によって plan / chunk / ticket を更新する
        - 必要なら `.canvas` を派生物として再同期する

        ## 初期 seed
        - 初期 block として `{seed_title}` を置く
        - {seed_action}
        """
    ).strip()


def render_human_manual(config: Config) -> str:
    protected = render_bullet_list(config.migration_protected_paths, "まだなし")
    return "\n".join(
        [
            "# Human Manual",
            "",
            "## この docs の目的",
            "- 人間がどこで判断し、何を AI に任せ、何を承認するかを明確にする",
            "",
            "## 人間が判断すること",
            "- 優先順位",
            "- 要求の採否",
            "- protected path を動かしてよいか",
            "- 旧 docs を正本から外してよいか",
            "",
            "## AI に任せること",
            "- inventory の初回ドラフト",
            "- gap の洗い出し",
            "- adoption plan の叩き台",
            "- block / chunk / ticket の更新",
            "",
            "## migration 時の確認ポイント",
            "- 現行 AI が `MIGRATION_START_HERE.md` を起点に作業しているか",
            "- `docs/migration/project-inventory.md` が埋まっているか",
            "- `docs/migration/gap-report.md` に open question が残っているか",
            "- `docs/migration/adoption-plan.md` に段階導入 plan があるか",
            "",
            "## protected path",
            protected,
        ]
    )


def render_attention_queue() -> str:
    seed_path = BUILDER_DOCS / "exec-plans" / "active" / "attention-queue.md"
    if seed_path.exists():
        return seed_path.read_text(encoding="utf-8").strip()
    return textwrap.dedent(
        """
        # ATTENTION Queue

        「今は実装しないが、後で必ず再注目する事項」を管理する台帳。

        ## Active Items
        | id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
        |---|---|---|---|---|---|---|---|

        ## Template
        | id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
        |---|---|---|---|---|---|---|---|
        | ATN-YYYY-MM-DD-XXX | pending | どの作業に入ったら再注目するか | 必須実装 / 必須確認事項 | 関連 docs へのリンク | YYYY-MM-DD | - | 補足 |
        """
    ).strip()


def render_project_intake(config: Config, plan_id: str, today: str) -> str:
    return textwrap.dedent(
        f"""
        # Project Intake

        - intake_id: INTAKE-{today}
        - parent_plan: {plan_id}
        - status: captured
        - last_updated: {today}

        ## 要求原文
        - {config.project_request}

        ## 成果物候補
        - {config.primary_deliverable or "未確定"}
        """
    ).strip()


def render_discovery_brief(config: Config, plan_id: str, today: str) -> str:
    confirmed = render_bullet_list(config.discovery_confirmed, "まだなし")
    assumptions = render_bullet_list(config.discovery_assumptions, "まだなし")
    non_goals = render_bullet_list(config.discovery_non_goals, "まだなし")
    constraints = render_bullet_list(config.discovery_constraints, "まだなし")
    return "\n".join(
        [
            "# Discovery Brief",
            "",
            f"- discovery_id: DISCOVERY-{today}",
            f"- parent_plan: {plan_id}",
            "- status: in_progress",
            f"- last_updated: {today}",
            "",
            "## 確定事項",
            confirmed,
            "",
            "## 仮置き前提",
            assumptions,
            "",
            "## 非目的",
            non_goals,
            "",
            "## 制約",
            constraints,
        ]
    )


def render_plan_spec(config: Config, plan_id: str, today: str) -> str:
    rows = []
    if config.seed_discovery_block:
        if config.migration_enabled:
            rows.append("| BLK-001 | 現行運用を棚卸しする | 既存 docs、受け渡し、保護 path を整理し、新 schema への写像方針を定義する | pending | - |")
        else:
            rows.append("| BLK-001 | 何を作るか決める | 人間要求を聞き取り、最初の実装可能 block 群を定義する | pending | - |")
    blocks_table = "\n".join(rows) if rows else ""
    if not blocks_table:
        blocks_table = "| | | | | |"
    return "\n".join(
        [
            "# Plan Spec",
            "",
            f"- plan_id: {plan_id}",
            "- status: pending",
            "- owner: プランオーナー",
            "- priority: high",
            f"- last_updated: {today}",
            f"- source_intake: INTAKE-{today}",
            f"- source_discovery: DISCOVERY-{today}",
            "",
            "## 目的",
            f"- {config.project_summary or config.project_request}",
            "",
            "## High-level blocks",
            "| block_id | title | goal | status | depends_on |",
            "|---|---|---|---|---|",
            blocks_table,
        ]
    )


def render_seed_block(config: Config, plan_id: str) -> str:
    if config.migration_enabled:
        return textwrap.dedent(
            f"""
            ---
            block_id: BLK-001
            parent_plan: {plan_id}
            status: pending
            title: 現行運用を棚卸しする
            kind: block
            ---

            # 現行運用を棚卸しする

            既存 docs、受け渡し、保護 path を整理し、新 schema への写像方針を定義する migration 用 seed block。

            ## Done チェック
            - [ ] `docs/migration/project-inventory.md` に現行 docs と artefact の棚卸しが入っている
            - [ ] `docs/migration/gap-report.md` に新 schema との差分が整理されている
            - [ ] `docs/migration/adoption-plan.md` に段階導入 plan が入っている
            - [ ] `docs/migration/current-ai-migration-request.md` を使った現行 AI への依頼結果が反映されている
            """
        ).strip()
    return textwrap.dedent(
        f"""
        ---
        block_id: BLK-001
        parent_plan: {plan_id}
        status: pending
        title: 何を作るか決める
        kind: block
        ---

        # 何を作るか決める

        人間要求を聞き取り、最初の実装可能 block 群を定義する discovery 用 seed block。

        ## Done チェック
        - [ ] 要求原文が `project-intake` に整理されている
        - [ ] `discovery-brief` に仮置き前提と未確定事項が分離されている
        - [ ] 後続の実装 block が `plan-spec` に追加されている
        """
    ).strip()


def render_migration_index() -> str:
    return textwrap.dedent(
        """
        # Migration Docs

        - [project-inventory.md](./project-inventory.md)
        - [gap-report.md](./gap-report.md)
        - [adoption-plan.md](./adoption-plan.md)
        - [current-ai-migration-request.md](./current-ai-migration-request.md)
        """
    ).strip()


def render_project_inventory(config: Config, plan_id: str, today: str) -> str:
    existing_docs_rows = render_table_rows(config.migration_existing_docs, "| {item} | existing_doc | 現行運用の参照物 | TBD |")
    notes = render_bullet_list(config.migration_notes, "まだなし")
    protected = render_bullet_list(config.migration_protected_paths, "まだなし")
    return "\n".join(
        [
            "# Project Inventory",
            "",
            f"- inventory_id: INVENTORY-{today}",
            f"- related_plan: {plan_id}",
            "- status: in_progress",
            "- owner: プランオーナー",
            f"- last_updated: {today}",
            "",
            "## 現在の運用要約",
            f"- {config.migration_current_state}",
            "",
            "## 既存 docs / artefact 棚卸し",
            "| path_or_location | kind | current_role | keep_or_replace |",
            "|---|---|---|---|",
            existing_docs_rows,
            "",
            "## 保護すべきもの",
            protected,
            "",
            "## 補足",
            notes,
        ]
    )


def render_gap_report(config: Config, plan_id: str, today: str) -> str:
    gap_rows = render_table_rows(
        config.migration_known_gaps,
        "| {item} | schema_mapping | 要対応 | plan-owner |",
        fallback="| まだなし | schema_mapping | 要確認 | plan-owner |",
    )
    return "\n".join(
        [
            "# Gap Report",
            "",
            f"- gap_report_id: GAP-{today}",
            f"- related_plan: {plan_id}",
            "- status: in_progress",
            "- owner: プランオーナー",
            f"- last_updated: {today}",
            "",
            "## 移行目的",
            f"- {config.migration_adoption_goal}",
            "",
            "## 現在の運用要約",
            f"- {config.migration_current_state}",
            "",
            "## Mapping Summary",
            "| current_item | gap_type | required_action | owner |",
            "|---|---|---|---|",
            gap_rows,
        ]
    )


def render_adoption_plan(config: Config, plan_id: str, today: str) -> str:
    protected = render_bullet_list(config.migration_protected_paths, "まだなし")
    return "\n".join(
        [
            "# Adoption Plan",
            "",
            f"- adoption_plan_id: ADOPT-{today}",
            f"- related_plan: {plan_id}",
            "- status: pending",
            "- owner: プランオーナー",
            f"- last_updated: {today}",
            "",
            "## 目的",
            f"- {config.migration_adoption_goal}",
            "",
            "## フェーズ",
            "| phase | goal | scope | exit_criteria | owner |",
            "|---|---|---|---|---|",
            "| 1 | 棚卸し完了 | inventory / gap-report | 現行 docs の mapping が揃う | plan-owner |",
            "| 2 | 正本の仮設置 | AGENTS / docs | core docs の置き場所が決まる | plan-owner |",
            "| 3 | planning 置換 | block / chunk / ticket | 新 schema で task 化できる | task-planner |",
            "",
            "## 保護条件",
            protected,
        ]
    )


def render_current_ai_migration_request(config: Config, plan_id: str, today: str) -> str:
    existing_docs = render_bullet_list(config.migration_existing_docs, "必要な既存 docs を棚卸しして追記する")
    protected = render_bullet_list(config.migration_protected_paths, "人間承認なしで破壊的変更をしない")
    notes = render_bullet_list(config.migration_notes, "まだなし")
    return "\n".join(
        [
            "# Current AI Migration Request",
            "",
            f"- request_id: MIGRATION-REQUEST-{today}",
            f"- related_plan: {plan_id}",
            "- status: ready",
            "- owner: プランオーナー",
            f"- last_updated: {today}",
            "",
            "あなたはこのプロジェクトの現行 docs / 運用を把握している AI です。  ",
            "以下の migration bootstrap を参照し、既存運用を新 schema へ写像してください。",
            "",
            "## 目的",
            f"- {config.migration_adoption_goal}",
            "",
            "## 現在の運用前提",
            f"- {config.migration_current_state}",
            "",
            "## 参照するもの",
            "- `docs/migration/project-inventory.md`",
            "- `docs/migration/gap-report.md`",
            "- `docs/migration/adoption-plan.md`",
            "- `docs/OPERATIONAL_SCHEMA.md`",
            "- `docs/ROLE_SKILLS.md`",
            "",
            "## 既存 docs 候補",
            existing_docs,
            "",
            "## 進め方",
            "### Step 1",
            "- 既存 docs と運用 artefact を棚卸しし、`docs/migration/project-inventory.md` を埋める",
            "- この step が終わったら、まだ次の step を実行せず、棚卸し結果を返す",
            "",
            "### Step 2",
            "- `docs/migration/project-inventory.md` を元に、現在の flow を `block / chunk / ticket` 相当へ写像する",
            "- 差分と open question を `docs/migration/gap-report.md` へ反映する",
            "- この step が終わったら、差分結果を返す",
            "",
            "### Step 3",
            "- `docs/migration/gap-report.md` を元に、導入順を `docs/migration/adoption-plan.md` に段階化する",
            "- 人間承認が必要な判断と protected path を明示する",
            "- この step が終わったら、導入 plan を返す",
            "",
            "## 禁止事項",
            protected,
            "",
            "## 返してほしいもの",
            "- Step 1 完了時: 埋まった `docs/migration/project-inventory.md`",
            "- Step 2 完了時: 埋まった `docs/migration/gap-report.md`",
            "- Step 3 完了時: 埋まった `docs/migration/adoption-plan.md`",
            "- 残っている open question",
            "",
            "## 補足",
            notes,
        ]
    )


def render_migration_start_here() -> str:
    return "\n".join(
        [
            "# MIGRATION START HERE",
            "",
            "現行 AI は、まず [docs/migration/current-ai-migration-request.md](./docs/migration/current-ai-migration-request.md) を読むこと。",
            "",
            "一度に全部やらず、step-by-step で進めること。",
            "",
            "最初にやるのは Step 1 だけです。",
            "1. `docs/migration/project-inventory.md` を埋める",
            "2. Step 1 の結果を返す",
            "3. 人間かプランオーナーの次指示を待つ",
            "",
            "破壊的な rename / delete は、人間承認なしで行わないこと。",
        ]
    )


def render_reference_seed(name: str) -> tuple[str, str] | None:
    seed = REFERENCE_SEED_MAP.get(name)
    if seed is None:
        return None
    reference_id, title, body = seed
    filename = f"{name.replace('_', '-')}.md"
    content = textwrap.dedent(
        f"""
        ---
        reference_id: {reference_id}
        title: {title}
        lane_order: {list(REFERENCE_SEED_MAP).index(name) * 100 + 100}
        kind: reference
        ---

        # {title}

        - {body}
        """
    ).strip()
    return filename, content


def render_bullet_list(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def render_table_rows(items: list[str], template: str, fallback: str = "| まだなし | - | - | - |") -> str:
    if not items:
        return fallback
    return "\n".join(template.format(item=item) for item in items)


def format_relative_path(root: Path, target: Path) -> str:
    try:
        relative = target.relative_to(root)
    except ValueError:
        return str(target)
    text = relative.as_posix()
    return text or "."


def build_managed_seed_sources(config: Config) -> dict[Path, list[str]]:
    if config.self_hosting_enabled:
        return {}
    return {
        config.output_root / "docs" / "PLANS.md": [BUILDER_DOCS.joinpath("PLANS.md").read_text(encoding="utf-8")],
        config.active_dir / "index.md": [
            BUILDER_DOCS.joinpath("exec-plans/active/index.md").read_text(encoding="utf-8")
        ],
        config.active_dir / "attention-queue.md": [
            BUILDER_DOCS.joinpath("exec-plans/active/attention-queue.md").read_text(encoding="utf-8")
        ],
        config.completed_dir / "index.md": [
            BUILDER_DOCS.joinpath("exec-plans/completed/index.md").read_text(encoding="utf-8")
        ],
        config.completed_dir / "progress-log.md": [
            BUILDER_DOCS.joinpath("exec-plans/completed/progress-log.md").read_text(encoding="utf-8")
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
