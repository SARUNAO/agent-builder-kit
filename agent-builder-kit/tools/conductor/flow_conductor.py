#!/usr/bin/env python3
"""Scaffold CLI for the `conductor` runtime."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, TypeVar


if (Path(__file__).resolve().parent.parent.parent / "docs").is_dir():
    REPO_ROOT = Path(__file__).resolve().parent.parent.parent
else:
    REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAN_SPEC = REPO_ROOT / "docs/exec-plans/plan-spec.md"
DEFAULT_BLOCK_DIR = REPO_ROOT / "docs/exec-plans/blocks"
DEFAULT_CHUNK_DIR = REPO_ROOT / "docs/exec-plans/chunks"
DEFAULT_TICKET_DIR = REPO_ROOT / "docs/exec-plans/tickets"
DEFAULT_OPERATOR_REQUEST_DIR = REPO_ROOT / "docs/exec-plans/operator-requests"
DEFAULT_REFERENCE_DIR = REPO_ROOT / "docs/references"
DEFAULT_CANVAS = REPO_ROOT / "docs/exec-plans/canvas/development-flow.canvas"
DEFAULT_RUNTIME_STATE_DIR = Path(tempfile.gettempdir()) / "agent_builder_automation_conductor"
DEFAULT_CANVAS_SYNC_SCRIPT = (
    REPO_ROOT / "tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py"
)
FRONTMATTER_BOUNDARY = "---"
META_RE = re.compile(r"^-\s+([A-Za-z0-9_-]+):\s*(.+?)\s*$")
CONFIRMATION_MARKER_RE = re.compile(r"^\s*(?:-\s+)?要確認:\s*(.+?)\s*$")
CONFIRMATION_MARKER_HEADING = "要確認 marker"
LOOP_RETRY_THRESHOLD = 3
LOOP_HISTORY_LIMIT = 6
DEFAULT_EXECUTION_LEVEL = "MID"
SUPPORTED_EXECUTION_LEVELS = ("MID", "HIGH")
BOUNDED_MULTI_STEP_DEFAULT_MAX_STEPS = 5
BOUNDED_MULTI_STEP_ALLOWED_ROLES = ("task_worker", "task_planner")
T = TypeVar("T")


@dataclass(frozen=True)
class ConductorArgs:
    plan_spec: Path
    block_dir: Path
    chunk_dir: Path
    ticket_dir: Path
    operator_request_dir: Path
    runtime_state_dir: Path
    level: str
    max_steps: int
    human: bool


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("max-steps は 1 以上の整数である必要があります。")
    return parsed


@dataclass(frozen=True)
class BlockState:
    block_id: str
    title: str
    goal: str
    status: str
    depends_on: str
    source_path: str


@dataclass(frozen=True)
class BlockNoteState:
    block_id: str
    title: str
    status: str
    checklist_complete: bool
    source_path: str


@dataclass(frozen=True)
class ChunkState:
    chunk_id: str
    parent_block: str
    title: str
    status: str
    depends_on: str
    checklist_complete: bool
    close_material_ready: bool
    source_path: str


@dataclass(frozen=True)
class TicketState:
    ticket_id: str
    parent_chunk: str
    title: str
    status: str
    depends_on: str
    checklist_complete: bool
    fact_report_exists: bool
    review_required: bool
    docs_only_skip: bool
    reviewer_findings_present: bool
    reviewer_resolution_present: bool
    reviewer_no_findings: bool
    source_path: str


@dataclass(frozen=True)
class OperatorRequestState:
    request_id: str
    status: str
    requested_role: str
    interrupt_mode: str
    source_path: str
    summary: str


def parse_args() -> ConductorArgs:
    parser = argparse.ArgumentParser(
        description="Scaffold CLI for the docs-driven `conductor` runtime."
    )
    parser.add_argument("--plan-spec", type=Path, default=DEFAULT_PLAN_SPEC)
    parser.add_argument("--block-dir", type=Path, default=DEFAULT_BLOCK_DIR)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--ticket-dir", type=Path, default=DEFAULT_TICKET_DIR)
    parser.add_argument(
        "--operator-request-dir",
        type=Path,
        default=DEFAULT_OPERATOR_REQUEST_DIR,
    )
    parser.add_argument(
        "--runtime-state-dir",
        type=Path,
        default=DEFAULT_RUNTIME_STATE_DIR,
        help="loop 判定用の runtime-local history を置く directory。",
    )
    parser.add_argument(
        "--level",
        choices=SUPPORTED_EXECUTION_LEVELS,
        default=DEFAULT_EXECUTION_LEVEL,
        help="conductor の execution level。既定は MID。",
    )
    parser.add_argument(
        "--max-steps",
        type=positive_int,
        default=BOUNDED_MULTI_STEP_DEFAULT_MAX_STEPS,
        help="same-block bounded run の最大 step 数。既定は 5。",
    )
    parser.add_argument(
        "--human",
        action="store_true",
        help="stdout JSON に加えて、人間向け summary を stderr へ出す。",
    )
    ns = parser.parse_args()
    return ConductorArgs(
        plan_spec=ns.plan_spec,
        block_dir=ns.block_dir,
        chunk_dir=ns.chunk_dir,
        ticket_dir=ns.ticket_dir,
        operator_request_dir=ns.operator_request_dir,
        runtime_state_dir=ns.runtime_state_dir,
        level=ns.level,
        max_steps=ns.max_steps,
        human=ns.human,
    )


def path_payload(path: Path) -> dict[str, str | bool]:
    kind = "missing"
    if path.exists():
        kind = "dir" if path.is_dir() else "file"
    return {
        "path": str(path),
        "exists": path.exists(),
        "kind": kind,
    }


def validate_args(args: ConductorArgs) -> None:
    if not args.plan_spec.exists():
        raise FileNotFoundError(f"plan-spec が見つかりません: {args.plan_spec}")
    if not args.plan_spec.is_file():
        raise ValueError(f"plan-spec は file である必要があります: {args.plan_spec}")

    dir_fields = (
        ("block-dir", args.block_dir),
        ("chunk-dir", args.chunk_dir),
        ("ticket-dir", args.ticket_dir),
        ("operator-request-dir", args.operator_request_dir),
    )
    for label, path in dir_fields:
        if not path.exists():
            raise FileNotFoundError(f"{label} が見つかりません: {path}")
        if not path.is_dir():
            raise ValueError(f"{label} は directory である必要があります: {path}")


def read_markdown(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def parse_frontmatter(lines: list[str]) -> dict[str, str]:
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == FRONTMATTER_BOUNDARY:
            return data
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return {}


def parse_metadata(lines: list[str]) -> dict[str, str]:
    data = parse_frontmatter(lines)
    if data:
        return data
    parsed: dict[str, str] = {}
    for line in lines:
        match = META_RE.match(line.strip())
        if match:
            parsed[match.group(1)] = match.group(2)
    return parsed


def first_heading(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def first_bullet_after_heading(lines: list[str], heading: str) -> str:
    target = f"## {heading}"
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == target:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            return ""
        if in_section and stripped.startswith("- "):
            return stripped[2:].strip()
    return ""


def iter_lines_in_section(
    lines: list[str],
    heading: str,
) -> list[tuple[int, str]]:
    target = f"## {heading}"
    in_section = False
    section_lines: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped == target:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section:
            section_lines.append((line_number, line))
    return section_lines


def section_text(lines: list[str], heading: str) -> str:
    return "\n".join(line for _, line in iter_lines_in_section(lines, heading))


def checklist_complete(lines: list[str]) -> bool:
    target = "## Done チェック"
    in_section = False
    found = False
    for line in lines:
        stripped = line.strip()
        if stripped == target:
            in_section = True
            found = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if in_section and stripped.startswith("- [") and not (
            stripped.startswith("- [x]") or stripped.startswith("- [X]")
        ):
            return False
    return found


def section_has_content(lines: list[str], heading: str) -> bool:
    target = f"## {heading}"
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped == target:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            return False
        if in_section and stripped:
            return True
    return False


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown_table(lines: list[str]) -> list[dict[str, str]]:
    if len(lines) < 2:
        return []
    headers = split_table_row(lines[0])
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        stripped = line.strip()
        if not stripped:
            continue
        cells = split_table_row(stripped)
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append({header: cells[idx] for idx, header in enumerate(headers)})
    return rows


def extract_table(lines: list[str], heading: str) -> list[dict[str, str]]:
    target = f"## {heading}"
    for idx, line in enumerate(lines):
        if line.strip() != target:
            continue
        table_lines: list[str] = []
        cursor = idx + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            table_lines.append(lines[cursor].strip())
            cursor += 1
        return parse_markdown_table(table_lines)
    return []


def parse_plan_spec(path: Path) -> tuple[dict[str, str], list[BlockState]]:
    lines = read_markdown(path)
    plan_meta = parse_metadata(lines)
    if "plan_id" not in plan_meta:
        raise ValueError(f"plan-spec から plan_id を読めません: {path}")
    block_rows = extract_table(lines, "High-level blocks")
    blocks: list[BlockState] = []
    for row in block_rows:
        block_id = row.get("block_id", "").strip()
        if not block_id:
            raise ValueError(f"plan-spec の block table に block_id が欠けています: {path}")
        blocks.append(
            BlockState(
                block_id=block_id,
                title=row.get("title", "").strip(),
                goal=row.get("goal", "").strip(),
                status=row.get("status", "").strip(),
                depends_on=row.get("depends_on", "-").strip() or "-",
                source_path=str(path),
            )
        )
    return plan_meta, blocks


def require_fields(meta: dict[str, str], required: tuple[str, ...], path: Path) -> None:
    missing = [field for field in required if not meta.get(field)]
    if missing:
        raise ValueError(f"{path} の frontmatter に必須項目がありません: {', '.join(missing)}")


def parse_chunk_states(path: Path) -> ChunkState:
    lines = read_markdown(path)
    meta = parse_frontmatter(lines)
    require_fields(meta, ("chunk_id", "parent_block", "title", "status"), path)
    return ChunkState(
        chunk_id=meta["chunk_id"],
        parent_block=meta["parent_block"],
        title=meta["title"],
        status=meta["status"],
        depends_on=meta.get("depends_on", "-"),
        checklist_complete=checklist_complete(lines),
        close_material_ready=section_has_content(lines, "chunk close 材料"),
        source_path=str(path),
    )


def fact_report_path_for_ticket(fact_report_dir: Path, ticket_id: str) -> Path:
    return fact_report_dir / f"fact-report-{ticket_id.lower()}.md"


def parse_ticket_states(path: Path, fact_report_dir: Path) -> TicketState:
    lines = read_markdown(path)
    meta = parse_frontmatter(lines)
    require_fields(meta, ("ticket_id", "parent_chunk", "status"), path)
    review_text = section_text(lines, "Review")
    normalized_review_text = review_text.lower()
    return TicketState(
        ticket_id=meta["ticket_id"],
        parent_chunk=meta["parent_chunk"],
        title=first_heading(lines) or path.stem,
        status=meta["status"],
        depends_on=meta.get("depends_on", "-"),
        checklist_complete=checklist_complete(lines),
        fact_report_exists=fact_report_path_for_ticket(
            fact_report_dir,
            meta["ticket_id"],
        ).exists(),
        review_required="reviewer handoff が必要" in review_text,
        docs_only_skip="docs-only skip" in normalized_review_text,
        reviewer_findings_present=section_has_content(lines, "Reviewer Findings"),
        reviewer_resolution_present=section_has_content(lines, "Reviewer Resolution"),
        reviewer_no_findings=(
            "重大 findings は無し" in review_text
            or "重大 findings はありません" in review_text
        ),
        source_path=str(path),
    )


def parse_block_note(path: Path) -> BlockNoteState:
    lines = read_markdown(path)
    meta = parse_frontmatter(lines)
    require_fields(meta, ("block_id", "status"), path)
    return BlockNoteState(
        block_id=meta["block_id"],
        title=meta.get("title", first_heading(lines) or path.stem),
        status=meta["status"],
        checklist_complete=checklist_complete(lines),
        source_path=str(path),
    )


def parse_operator_request(path: Path) -> OperatorRequestState:
    lines = read_markdown(path)
    meta = parse_frontmatter(lines)
    require_fields(meta, ("request_id", "status", "requested_role", "interrupt_mode"), path)
    return OperatorRequestState(
        request_id=meta["request_id"],
        status=meta["status"],
        requested_role=meta["requested_role"],
        interrupt_mode=meta["interrupt_mode"],
        source_path=str(path),
        summary=first_bullet_after_heading(lines, "summary"),
    )


def load_dir_states(directory: Path, parser: Callable[[Path], T]) -> list[T]:
    return [parser(path) for path in sorted(directory.glob("*.md"))]


def summarize_status(items: list[object]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        status = getattr(item, "status")
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_status_map(items: list[object], id_field: str) -> dict[str, str]:
    return {getattr(item, id_field): getattr(item, "status") for item in items}


def detect_block_note_mismatches(
    blocks: list[BlockState],
    block_notes: list[BlockNoteState],
) -> list[dict[str, str]]:
    note_map = {item.block_id: item for item in block_notes}
    mismatches: list[dict[str, str]] = []
    for block in blocks:
        note = note_map.get(block.block_id)
        if note is None:
            continue
        if note.status != block.status:
            mismatches.append(
                {
                    "entity_type": "block",
                    "entity_id": block.block_id,
                    "frontmatter_status": note.status,
                    "table_status": block.status,
                    "table_source_path": block.source_path,
                    "frontmatter_source_path": note.source_path,
                }
            )
    return mismatches


def detect_chunk_table_mismatches(
    chunks: list[ChunkState],
    tickets: list[TicketState],
) -> list[dict[str, str]]:
    ticket_status_map = build_status_map(tickets, "ticket_id")
    mismatches: list[dict[str, str]] = []
    for chunk in chunks:
        lines = read_markdown(Path(chunk.source_path))
        table_rows = extract_table(lines, "含む ticket")
        for row in table_rows:
            ticket_id = row.get("ticket_id", "").strip()
            table_status = row.get("status", "").strip()
            if not ticket_id or ticket_id not in ticket_status_map:
                continue
            if ticket_status_map[ticket_id] != table_status:
                mismatches.append(
                    {
                        "entity_type": "ticket",
                        "entity_id": ticket_id,
                        "parent_chunk": chunk.chunk_id,
                        "frontmatter_status": ticket_status_map[ticket_id],
                        "table_status": table_status,
                        "table_source_path": chunk.source_path,
                    }
                )
    return mismatches


def build_promotion_candidates(
    blocks: list[BlockState],
    block_notes: list[BlockNoteState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
) -> dict[str, list[dict[str, str]]]:
    tickets_by_chunk: dict[str, list[TicketState]] = {}
    for ticket in tickets:
        tickets_by_chunk.setdefault(ticket.parent_chunk, []).append(ticket)

    chunks_by_block: dict[str, list[ChunkState]] = {}
    for chunk in chunks:
        chunks_by_block.setdefault(chunk.parent_block, []).append(chunk)

    ticket_candidates: list[dict[str, str]] = []
    for ticket in tickets:
        if ticket.status == "done":
            continue
        if ticket.checklist_complete and ticket.fact_report_exists:
            ticket_candidates.append(
                {
                    "entity_type": "ticket",
                    "entity_id": ticket.ticket_id,
                    "reason": "Done チェックと fact-report が揃っている",
                    "source_path": ticket.source_path,
                }
            )

    chunk_candidates: list[dict[str, str]] = []
    for chunk in chunks:
        child_tickets = tickets_by_chunk.get(chunk.chunk_id, [])
        if chunk.status == "done" or not child_tickets:
            continue
        if all(ticket.status == "done" for ticket in child_tickets) and chunk.checklist_complete:
            reason = "配下 ticket がすべて done で Done チェックが揃っている"
            if chunk.close_material_ready:
                reason += "。chunk close 材料もある"
            chunk_candidates.append(
                {
                    "entity_type": "chunk",
                    "entity_id": chunk.chunk_id,
                    "reason": reason,
                    "source_path": chunk.source_path,
                }
            )

    block_note_map = {item.block_id: item for item in block_notes}
    block_candidates: list[dict[str, str]] = []
    for block in blocks:
        child_chunks = chunks_by_block.get(block.block_id, [])
        note = block_note_map.get(block.block_id)
        if block.status == "done" or not child_chunks or note is None:
            continue
        if all(chunk.status == "done" for chunk in child_chunks) and note.checklist_complete:
            block_candidates.append(
                {
                    "entity_type": "block",
                    "entity_id": block.block_id,
                    "reason": "配下 chunk がすべて done で block note の Done チェックが揃っている",
                    "source_path": note.source_path,
                }
            )

    return {
        "tickets": ticket_candidates,
        "chunks": chunk_candidates,
        "blocks": block_candidates,
    }


def build_sync_warnings(
    blocks: list[BlockState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
    table_mismatches: list[dict[str, str]],
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []

    tickets_by_chunk: dict[str, list[TicketState]] = {}
    for ticket in tickets:
        tickets_by_chunk.setdefault(ticket.parent_chunk, []).append(ticket)

    chunks_by_block: dict[str, list[ChunkState]] = {}
    for chunk in chunks:
        chunks_by_block.setdefault(chunk.parent_block, []).append(chunk)

    for chunk in chunks:
        child_tickets = tickets_by_chunk.get(chunk.chunk_id, [])
        if not child_tickets:
            continue
        if chunk.status != "done" and all(ticket.status == "done" for ticket in child_tickets):
            warnings.append(
                {
                    "code": "chunk_status_stale",
                    "entity_type": "chunk",
                    "entity_id": chunk.chunk_id,
                    "message": "配下 ticket はすべて done だが、chunk status がまだ done ではありません。",
                    "source_path": chunk.source_path,
                }
            )

    for block in blocks:
        child_chunks = chunks_by_block.get(block.block_id, [])
        if not child_chunks:
            continue
        if block.status != "done" and all(chunk.status == "done" for chunk in child_chunks):
            warnings.append(
                {
                    "code": "block_status_stale",
                    "entity_type": "block",
                    "entity_id": block.block_id,
                    "message": "配下 chunk はすべて done だが、block status がまだ done ではありません。",
                    "source_path": block.source_path,
                }
            )

    for mismatch in table_mismatches:
        warnings.append(
            {
                "code": "table_frontmatter_mismatch",
                "entity_type": mismatch["entity_type"],
                "entity_id": mismatch["entity_id"],
                "message": "table と frontmatter の status が一致していません。",
                "source_path": mismatch["table_source_path"],
            }
        )

    return warnings


def build_advisories(
    route_hint: str,
    promotion_candidates: dict[str, list[dict[str, str]]],
    sync_warnings: list[dict[str, str]],
) -> list[dict[str, str]]:
    if route_hint not in {"task_worker", "task_planner"}:
        return []

    target_role = route_hint
    followup_role = "task_planner"
    advisories: list[dict[str, str]] = []

    for item in sync_warnings:
        advisories.append(
            {
                "code": "sync_warning_advisory",
                "severity": "advisory",
                "target_role": target_role,
                "followup_role": followup_role,
                "entity_type": item["entity_type"],
                "entity_id": item["entity_id"],
                "message": item["message"],
                "action": "現在の作業は継続してよいが、区切りで task-planner に同期漏れを伝える。",
                "source_path": item["source_path"],
            }
        )

    for group_name in ("tickets", "chunks", "blocks"):
        for item in promotion_candidates[group_name]:
            advisories.append(
                {
                    "code": "promotion_candidate_advisory",
                    "severity": "advisory",
                    "target_role": target_role,
                    "followup_role": followup_role,
                    "entity_type": item["entity_type"],
                    "entity_id": item["entity_id"],
                    "message": item["reason"],
                    "action": "現在の作業を止める必要はないが、task-planner に昇格候補として引き継ぐ。",
                    "source_path": item["source_path"],
                }
            )

    return advisories


def sorted_values(values: list[str]) -> list[str]:
    return sorted(value for value in values if value)


def advisory_fingerprint(advisories: list[dict[str, str]]) -> list[str]:
    return sorted_values(
        [
            ":".join(
                [
                    item.get("code", ""),
                    item.get("target_role", ""),
                    item.get("followup_role", ""),
                    item.get("entity_type", ""),
                    item.get("entity_id", ""),
                ]
            )
            for item in advisories
        ]
    )


def promotion_candidate_fingerprint(
    promotion_candidates: dict[str, list[dict[str, str]]],
) -> list[str]:
    fingerprints: list[str] = []
    for group_name in ("tickets", "chunks", "blocks"):
        for item in promotion_candidates[group_name]:
            fingerprints.append(
                ":".join(
                    [
                        group_name,
                        item.get("entity_type", ""),
                        item.get("entity_id", ""),
                    ]
                )
            )
    return sorted_values(fingerprints)


def build_gateway_signature(
    route_hint: str,
    blocks: list[BlockState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
    pending_requests: list[OperatorRequestState],
    advisories: list[dict[str, str]],
    promotion_candidates: dict[str, list[dict[str, str]]],
) -> dict[str, object]:
    return {
        "route_hint": route_hint,
        "active_block_ids": sorted_values(
            [item.block_id for item in blocks if item.status == "in_progress"]
        ),
        "active_chunk_ids": sorted_values(
            [item.chunk_id for item in chunks if item.status == "in_progress"]
        ),
        "active_ticket_ids": sorted_values(
            [item.ticket_id for item in tickets if item.status == "in_progress"]
        ),
        "pending_request_ids": sorted_values([item.request_id for item in pending_requests]),
        "advisory_fingerprint": advisory_fingerprint(advisories),
        "promotion_candidate_fingerprint": promotion_candidate_fingerprint(
            promotion_candidates
        ),
    }


def runtime_history_path(runtime_state_dir: Path, plan_spec: Path) -> Path:
    plan_key = hashlib.sha1(str(plan_spec.resolve()).encode("utf-8")).hexdigest()[:16]
    return runtime_state_dir / f"gateway-history-{plan_key}.json"


def infer_runtime_state_scope(runtime_state_dir: Path) -> str:
    try:
        if runtime_state_dir.resolve() == DEFAULT_RUNTIME_STATE_DIR.resolve():
            return "shared"
    except FileNotFoundError:
        if runtime_state_dir == DEFAULT_RUNTIME_STATE_DIR:
            return "shared"
    return "isolated"


def load_runtime_history(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    observations = payload.get("observations")
    if not isinstance(observations, list):
        return []
    return [item for item in observations if isinstance(item, dict)]


def observe_gateway_signature(
    runtime_state_dir: Path,
    plan_spec: Path,
    gateway_signature: dict[str, object],
) -> dict[str, object]:
    history_path = runtime_history_path(runtime_state_dir, plan_spec)
    state_scope = infer_runtime_state_scope(runtime_state_dir)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    signature_json = json.dumps(
        gateway_signature,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    signature_hash = hashlib.sha1(signature_json.encode("utf-8")).hexdigest()
    lock_path = history_path.with_suffix(".lock")
    with lock_path.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        observations = load_runtime_history(history_path)
        previous_hash = observations[-1].get("signature_hash") if observations else None
        previous_count = observations[-1].get("consecutive_count", 0) if observations else 0
        consecutive_count = int(previous_count) + 1 if previous_hash == signature_hash else 1
        observations.append(
            {
                "signature_hash": signature_hash,
                "gateway_signature": gateway_signature,
                "consecutive_count": consecutive_count,
            }
        )
        trimmed = observations[-LOOP_HISTORY_LIMIT:]
        temp_path = history_path.with_suffix(".tmp")
        temp_path.write_text(
            json.dumps(
                {
                    "observations": trimmed,
                    "history_limit": LOOP_HISTORY_LIMIT,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temp_path.replace(history_path)
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
    return {
        "signature_hash": signature_hash,
        "gateway_signature": gateway_signature,
        "consecutive_count": consecutive_count,
        "threshold": LOOP_RETRY_THRESHOLD,
        "history_limit": LOOP_HISTORY_LIMIT,
        "history_path": str(history_path),
        "runtime_state_scope": state_scope,
        "runtime_state_dir": str(runtime_state_dir),
    }


def parse_confirmation_marker_fields(payload: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for segment in payload.split(";"):
        stripped = segment.strip()
        if not stripped or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def extract_confirmation_candidates(
    path: Path,
    source_type: str,
    source_id: str,
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    lines = read_markdown(path)
    for line_number, line in iter_lines_in_section(lines, CONFIRMATION_MARKER_HEADING):
        match = CONFIRMATION_MARKER_RE.match(line)
        if not match:
            continue
        fields = parse_confirmation_marker_fields(match.group(1))
        key = fields.get("key", "")
        bundle = fields.get("bundle", "")
        next_role = fields.get("next_role", "plan_manager")
        requires_bundle = fields.get("requires_bundle", "").lower() == "true"
        if not key or not bundle or not requires_bundle or next_role != "plan_manager":
            continue
        candidates.append(
            {
                "key": key,
                "bundle": bundle,
                "next_role": next_role,
                "summary": fields.get("summary", ""),
                "source_type": source_type,
                "source_id": source_id,
                "source_path": str(path),
                "line_number": line_number,
            }
        )
    return candidates


def collect_confirmation_candidates(
    blocks: list[BlockState],
    block_notes: list[BlockNoteState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
    pending_requests: list[OperatorRequestState],
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    active_block_ids = {item.block_id for item in blocks if item.status == "in_progress"}
    block_note_map = {item.block_id: item for item in block_notes}
    for block_id in sorted(active_block_ids):
        note = block_note_map.get(block_id)
        if note is None:
            continue
        candidates.extend(
            extract_confirmation_candidates(Path(note.source_path), "block", block_id)
        )

    for chunk in chunks:
        if chunk.status == "in_progress":
            candidates.extend(
                extract_confirmation_candidates(
                    Path(chunk.source_path),
                    "chunk",
                    chunk.chunk_id,
                )
            )

    for ticket in tickets:
        if ticket.status == "in_progress":
            candidates.extend(
                extract_confirmation_candidates(
                    Path(ticket.source_path),
                    "ticket",
                    ticket.ticket_id,
                )
            )

    for request in pending_requests:
        candidates.extend(
            extract_confirmation_candidates(
                Path(request.source_path),
                "operator_request",
                request.request_id,
            )
        )

    return candidates


def build_bundled_confirmation_stop_reason(
    confirmation_candidates: list[dict[str, object]],
) -> dict[str, object] | None:
    bundles: dict[str, dict[str, dict[str, object]]] = {}
    for candidate in confirmation_candidates:
        bundle = str(candidate["bundle"])
        key = str(candidate["key"])
        bundles.setdefault(bundle, {})
        bundles[bundle].setdefault(key, candidate)

    viable_bundles: list[tuple[str, list[dict[str, object]]]] = []
    for bundle, key_map in bundles.items():
        unique_candidates = sorted(
            key_map.values(),
            key=lambda item: (
                str(item["source_type"]),
                str(item["source_id"]),
                str(item["key"]),
            ),
        )
        if len(unique_candidates) >= 2:
            viable_bundles.append((bundle, unique_candidates))

    if not viable_bundles:
        return None

    viable_bundles.sort(key=lambda item: (-len(item[1]), item[0]))
    bundle, candidates = viable_bundles[0]
    keys = [str(item["key"]) for item in candidates]
    return {
        "code": "bundled_confirmations_detected",
        "message": (
            f"bundle {bundle} に独立 confirmation key が {len(keys)} 件あり、"
            "仕様束の裁定が必要なため、自動続行を止めて plan-manager へ戻します。"
        ),
        "next_role": "plan_manager",
        "evidence": {
            "bundle": bundle,
            "keys": keys,
            "candidate_count": len(keys),
            "candidates": candidates,
        },
    }


def build_close_ready_handoff(
    args: ConductorArgs,
    blocks: list[BlockState],
    block_notes: list[BlockNoteState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
) -> dict[str, object]:
    active_tickets = [ticket for ticket in tickets if ticket.status == "in_progress"]
    if active_tickets:
        eligible_tickets = [
            ticket for ticket in active_tickets if ticket.checklist_complete and ticket.fact_report_exists
        ]
        triggered = len(eligible_tickets) == len(active_tickets)
        focus = eligible_tickets[0] if eligible_tickets else active_tickets[0]
        reason = (
            "active ticket が close-ready で、次の runnable item へ進む前に "
            "task-planner の source docs sync が必要。"
            if triggered
            else "active ticket は残っているが、まだ close-ready ではない。"
        )
        return {
            "eligible": triggered,
            "triggered": triggered,
            "next_role": "task_planner" if triggered else "task_worker",
            "entity_type": "ticket",
            "entity_id": focus.ticket_id,
            "reason": reason,
            "source_path": focus.source_path,
        }

    tickets_by_chunk: dict[str, list[TicketState]] = {}
    for ticket in tickets:
        tickets_by_chunk.setdefault(ticket.parent_chunk, []).append(ticket)

    active_chunks = [chunk for chunk in chunks if chunk.status == "in_progress"]
    if active_chunks:
        eligible_chunks: list[ChunkState] = []
        for chunk in active_chunks:
            child_tickets = tickets_by_chunk.get(chunk.chunk_id, [])
            if (
                child_tickets
                and chunk.checklist_complete
                and all(ticket.status == "done" for ticket in child_tickets)
            ):
                eligible_chunks.append(chunk)
        triggered = len(eligible_chunks) == len(active_chunks) and bool(eligible_chunks)
        focus = eligible_chunks[0] if eligible_chunks else active_chunks[0]
        reason = (
            "active chunk が close-ready で、次の runnable item へ進む前に "
            "task-planner の source docs sync が必要。"
            if triggered
            else "active chunk は残っているが、まだ close-ready ではない。"
        )
        return {
            "eligible": triggered,
            "triggered": triggered,
            "next_role": "task_planner" if triggered else "task_planner",
            "entity_type": "chunk",
            "entity_id": focus.chunk_id,
            "reason": reason,
            "source_path": focus.source_path,
        }

    block_note_map = {item.block_id: item for item in block_notes}
    chunks_by_block: dict[str, list[ChunkState]] = {}
    for chunk in chunks:
        chunks_by_block.setdefault(chunk.parent_block, []).append(chunk)

    active_blocks = [block for block in blocks if block.status == "in_progress"]
    if active_blocks:
        eligible_blocks: list[BlockState] = []
        for block in active_blocks:
            note = block_note_map.get(block.block_id)
            child_chunks = chunks_by_block.get(block.block_id, [])
            if (
                note
                and note.checklist_complete
                and child_chunks
                and all(chunk.status == "done" for chunk in child_chunks)
            ):
                eligible_blocks.append(block)
        triggered = len(eligible_blocks) == len(active_blocks) and bool(eligible_blocks)
        focus = eligible_blocks[0] if eligible_blocks else active_blocks[0]
        reason = (
            "active block が close-ready で、block `done` 昇格権限を持つ "
            "plan-manager 返送を優先する。"
            if triggered
            else "active block は残っているが、まだ close-ready ではない。"
        )
        return {
            "eligible": triggered,
            "triggered": triggered,
            "next_role": "plan_manager",
            "entity_type": "block",
            "entity_id": focus.block_id,
            "reason": reason,
            "source_path": focus.source_path,
        }

    return {
        "eligible": False,
        "triggered": False,
        "next_role": "plan_manager",
        "entity_type": "",
        "entity_id": "",
        "reason": "active frontier はありません。",
        "source_path": "",
    }


def build_reviewer_pass_through(
    tickets: list[TicketState],
) -> dict[str, object]:
    active_tickets = [ticket for ticket in tickets if ticket.status == "in_progress"]
    if not active_tickets:
        return {
            "eligible": False,
            "triggered": False,
            "blocking": False,
            "next_role": "task_worker",
            "entity_type": "",
            "entity_id": "",
            "reason": "active ticket が無いため、reviewer pass-through の対象が無い。",
            "source_path": "",
            "state": "inactive",
        }

    reviewable_tickets = [
        ticket
        for ticket in active_tickets
        if ticket.review_required
        and not ticket.docs_only_skip
        and ticket.fact_report_exists
    ]
    if not reviewable_tickets:
        focus = active_tickets[0]
        return {
            "eligible": False,
            "triggered": False,
            "blocking": False,
            "next_role": "task_worker",
            "entity_type": "ticket",
            "entity_id": focus.ticket_id,
            "reason": "active ticket は reviewer pass-through ready ではない。",
            "source_path": focus.source_path,
            "state": "inactive",
        }

    unresolved_findings = [
        ticket
        for ticket in reviewable_tickets
        if ticket.reviewer_findings_present
        and not ticket.reviewer_resolution_present
        and not ticket.reviewer_no_findings
    ]
    if unresolved_findings:
        focus = unresolved_findings[0]
        return {
            "eligible": True,
            "triggered": False,
            "blocking": True,
            "next_role": "task_worker",
            "entity_type": "ticket",
            "entity_id": focus.ticket_id,
            "reason": "reviewer finding が未解消のため、この bounded run はここで止めて task-worker へ返す。",
            "source_path": focus.source_path,
            "state": "blocking_findings",
        }

    ready_for_review = [
        ticket
        for ticket in reviewable_tickets
        if not ticket.reviewer_findings_present
        and not ticket.reviewer_resolution_present
        and not ticket.reviewer_no_findings
    ]
    if ready_for_review and len(ready_for_review) == len(reviewable_tickets):
        focus = ready_for_review[0]
        return {
            "eligible": True,
            "triggered": True,
            "blocking": False,
            "next_role": "reviewer",
            "entity_type": "ticket",
            "entity_id": focus.ticket_id,
            "reason": "code ticket が close-ready で reviewer handoff に入ったため、same-turn bounded run の internal role として reviewer を通す。",
            "source_path": focus.source_path,
            "state": "ready_for_review",
        }

    focus = reviewable_tickets[0]
    return {
        "eligible": True,
        "triggered": False,
        "blocking": False,
        "next_role": "task_planner",
        "entity_type": "ticket",
        "entity_id": focus.ticket_id,
        "reason": "reviewer pass-through は完了済みなので、次は frontier sync を優先する。",
        "source_path": focus.source_path,
        "state": "review_complete",
    }


def build_high_cross_block_handoff(
    args: ConductorArgs,
    blocks: list[BlockState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
) -> dict[str, object]:
    active_tickets = [ticket for ticket in tickets if ticket.status == "in_progress"]
    active_chunks = [chunk for chunk in chunks if chunk.status == "in_progress"]
    active_blocks = [block for block in blocks if block.status == "in_progress"]

    if args.level not in {"MID", "HIGH"}:
        return {
            "allowed": False,
            "eligible": False,
            "triggered": False,
            "next_role": "plan_manager",
            "entity_type": "",
            "entity_id": "",
            "reason": "execution_level が handoff 対象外のため、block-only handoff は無効。",
            "source_path": "",
        }

    if active_tickets:
        focus = active_tickets[0]
        return {
            "allowed": True,
            "eligible": False,
            "triggered": False,
            "next_role": "task_worker",
            "entity_type": "ticket",
            "entity_id": focus.ticket_id,
            "reason": "active ticket があるため、まず current frontier を優先する。",
            "source_path": focus.source_path,
        }

    if active_chunks:
        focus = active_chunks[0]
        return {
            "allowed": True,
            "eligible": False,
            "triggered": False,
            "next_role": "task_planner",
            "entity_type": "chunk",
            "entity_id": focus.chunk_id,
            "reason": "active chunk があるため、block-only handoff ではなく current frontier を優先する。",
            "source_path": focus.source_path,
        }

    if not active_blocks:
        return {
            "allowed": True,
            "eligible": False,
            "triggered": False,
            "next_role": "plan_manager",
            "entity_type": "",
            "entity_id": "",
            "reason": "active block が無いため、HIGH cross-block handoff の対象が無い。",
            "source_path": "",
        }

    if len(active_blocks) != 1:
        focus = active_blocks[0]
        return {
            "allowed": True,
            "eligible": False,
            "triggered": False,
            "next_role": "plan_manager",
            "entity_type": "block",
            "entity_id": focus.block_id,
            "reason": "active block が複数あるため、HIGH handoff ではなく plan-manager の裁定が必要。",
            "source_path": focus.source_path,
        }

    focus = active_blocks[0]
    child_chunks = [chunk for chunk in chunks if chunk.parent_block == focus.block_id]
    if child_chunks:
        return {
            "allowed": True,
            "eligible": False,
            "triggered": False,
            "next_role": "plan_manager",
            "entity_type": "block",
            "entity_id": focus.block_id,
            "reason": (
                "active block に child chunk が既にあるため、"
                "HIGH cross-block handoff ではなく plan-manager 境界を優先する。"
            ),
            "source_path": focus.source_path,
        }

    return {
        "allowed": True,
        "eligible": True,
        "triggered": True,
        "next_role": "task_planner",
        "entity_type": "block",
        "entity_id": focus.block_id,
        "reason": (
            f"execution_level={args.level} で active block だけが残っているため、"
            "child chunk 未生成の block-only 状態から次 block の chunk / ticket 生成へ進む "
            "narrow handoff として task-planner へ返す。"
        ),
        "source_path": focus.source_path,
    }


def infer_route_hint(
    pending_requests: list[OperatorRequestState],
    tickets: list[TicketState],
    chunks: list[ChunkState],
    promotion_candidates: dict[str, list[dict[str, str]]],
    sync_warnings: list[dict[str, str]],
    close_ready_handoff: dict[str, object],
    high_cross_block_handoff: dict[str, object],
    reviewer_pass_through: dict[str, object],
) -> str:
    if pending_requests:
        return "task_planner"
    if bool(reviewer_pass_through.get("blocking")):
        return "task_worker"
    if bool(close_ready_handoff.get("triggered")):
        return str(close_ready_handoff.get("next_role") or "task_planner")
    if bool(high_cross_block_handoff.get("triggered")):
        return str(high_cross_block_handoff.get("next_role") or "task_planner")
    if any(ticket.status == "in_progress" for ticket in tickets):
        return "task_worker"
    if any(promotion_candidates.values()) or sync_warnings:
        return "task_planner"
    if any(chunk.status == "in_progress" for chunk in chunks):
        return "task_planner"
    return "plan_manager"


def build_stop_reason(
    pending_requests: list[OperatorRequestState],
    bundled_confirmation_stop_reason: dict[str, object] | None,
    loop_stop_reason: dict[str, object] | None,
) -> dict[str, object] | None:
    if pending_requests:
        return {
            "code": "pending_operator_request",
            "message": "pending operator request があるため、自動続行せず task-planner へ戻します。",
            "next_role": "task_planner",
            "request_ids": [item.request_id for item in pending_requests],
            "evidence": {
                "pending_count": len(pending_requests),
                "request_ids": [item.request_id for item in pending_requests],
            },
        }
    if bundled_confirmation_stop_reason is not None:
        return bundled_confirmation_stop_reason
    return loop_stop_reason


def build_loop_stop_reason(
    route_hint: str,
    blocks: list[BlockState],
    chunks: list[ChunkState],
    tickets: list[TicketState],
    observation: dict[str, object],
) -> dict[str, object] | None:
    if route_hint not in {"task_worker", "task_planner"}:
        return None
    observed_count = int(observation["consecutive_count"])
    threshold = int(observation["threshold"])
    if observed_count < threshold:
        return None

    repeated_entities: list[dict[str, str]] = []
    for ticket in tickets:
        if ticket.status == "in_progress":
            repeated_entities.append(
                {"entity_type": "ticket", "entity_id": ticket.ticket_id}
            )
    if not repeated_entities:
        for chunk in chunks:
            if chunk.status == "in_progress":
                repeated_entities.append(
                    {"entity_type": "chunk", "entity_id": chunk.chunk_id}
                )
    if not repeated_entities:
        for block in blocks:
            if block.status == "in_progress":
                repeated_entities.append(
                    {"entity_type": "block", "entity_id": block.block_id}
                )
    if not repeated_entities:
        return None

    focus = repeated_entities[0]
    return {
        "code": "loop_retry_detected",
        "message": (
            f"{observation['runtime_state_scope']} runtime state で "
            f"{focus['entity_type']} {focus['entity_id']} を含む同一 gateway_signature が "
            f"{observed_count} 回連続で観測されたため、自動続行を止めて task-planner へ戻します。"
        ),
        "next_role": "task_planner",
        "evidence": {
            "observed_count": observed_count,
            "threshold": threshold,
            "gateway_signature": observation["gateway_signature"],
            "signature_hash": observation["signature_hash"],
            "repeated_entities": repeated_entities,
            "history_limit": observation["history_limit"],
            "history_path": observation["history_path"],
            "runtime_state_scope": observation["runtime_state_scope"],
            "runtime_state_dir": observation["runtime_state_dir"],
        },
    }


def infer_dispatchable(
    route_hint: str,
    stop_reason: dict[str, object] | None,
) -> bool:
    if stop_reason is not None:
        return False
    return route_hint in BOUNDED_MULTI_STEP_ALLOWED_ROLES


def build_bounded_multi_step_state(
    route_hint: str,
    stop_reason: dict[str, object] | None,
    blocks: list[BlockState],
    args: ConductorArgs,
    high_cross_block_handoff: dict[str, object],
) -> dict[str, object]:
    active_block_ids = [block.block_id for block in blocks if block.status == "in_progress"]
    return {
        "enabled": True,
        "same_block_only": not bool(high_cross_block_handoff.get("allowed")),
        "execution_level": args.level,
        "default_execution_level": DEFAULT_EXECUTION_LEVEL,
        "max_steps_per_run": args.max_steps,
        "default_max_steps_per_run": BOUNDED_MULTI_STEP_DEFAULT_MAX_STEPS,
        "step_override_active": args.max_steps != BOUNDED_MULTI_STEP_DEFAULT_MAX_STEPS,
        "allowed_roles": list(BOUNDED_MULTI_STEP_ALLOWED_ROLES),
        "return_boundary_roles": ["plan_manager"],
        "reviewer_direct_dispatch": False,
        "stop_conditions": [
            "stop_reason_not_null",
            "dispatchable_false",
            "route_hint_plan_manager",
            "reviewer_pass_through_blocking",
            "active_block_changed",
            "max_steps_reached",
        ],
        "active_block_ids": active_block_ids,
        "current_route_hint": route_hint,
        "current_step_dispatchable": (
            stop_reason is None and route_hint in BOUNDED_MULTI_STEP_ALLOWED_ROLES
        ),
        "cross_block_handoff_policy": (
            "mid_high_task_planner_only"
            if bool(high_cross_block_handoff.get("allowed"))
            else "disabled"
        ),
        "high_cross_block_handoff_allowed": bool(high_cross_block_handoff.get("allowed")),
        "high_cross_block_handoff_triggered": bool(high_cross_block_handoff.get("triggered")),
    }


def build_limited_actions(
    stop_reason: dict[str, object] | None,
    advisories: list[dict[str, str]],
) -> dict[str, dict[str, object]]:
    canvas_sync_available = (
        DEFAULT_CANVAS_SYNC_SCRIPT.exists()
        and DEFAULT_CANVAS.exists()
        and DEFAULT_PLAN_SPEC.exists()
        and DEFAULT_BLOCK_DIR.exists()
        and DEFAULT_CHUNK_DIR.exists()
        and DEFAULT_TICKET_DIR.exists()
    )
    canvas_sync_recommended = canvas_sync_available and stop_reason is None and bool(advisories)
    canvas_reason = "source docs を更新した role の sync を置き換えず、補助導線としてだけ使う。"
    if stop_reason is not None:
        canvas_reason = "hard stop があるため、この turn では補助 `.canvas` sync を優先しない。"
    elif not canvas_sync_available:
        canvas_reason = "必要な `.canvas` sync script または path が見つからない。"

    return {
        "status_sync": {
            "allowed": True,
            "mode": "mechanical_only",
            "scope": ["pending_to_in_progress"],
            "execute_now": False,
            "reason": "roll-up 整合のための機械同期だけを許し、done 昇格や意味変更は許さない。",
        },
        "canvas_sync": {
            "allowed": True,
            "mode": "supplemental_opt_in",
            "execute_now": False,
            "available": canvas_sync_available,
            "recommended": canvas_sync_recommended,
            "requires_explicit_opt_in": True,
            "reason": canvas_reason,
            "script_path": str(DEFAULT_CANVAS_SYNC_SCRIPT),
            "canvas_path": str(DEFAULT_CANVAS),
            "reference_dir": str(DEFAULT_REFERENCE_DIR),
        },
    }


def build_human_summary(response: dict[str, object]) -> str:
    route_hint = response["route_hint"]
    pending_requests = response["operator_requests"]["pending_count"]
    promotion_candidates = response["promotion_candidates"]
    sync_warnings = response["sync_warnings"]
    close_ready_handoff = response["close_ready_handoff"]
    high_cross_block_handoff = response["high_cross_block_handoff"]
    reviewer_pass_through = response["reviewer_pass_through"]
    stop_reason = response["stop_reason"]
    advisories = response["advisories"]
    limited_actions = response["limited_actions"]
    bounded_multi_step = response["bounded_multi_step"]
    summary_next_role = route_hint
    if stop_reason and stop_reason.get("next_role"):
        summary_next_role = str(stop_reason["next_role"])

    lines = [
        "# Conductor Summary",
        f"- gateway_mode: {response['gateway_mode']}",
        f"- next_role: {summary_next_role}",
        f"- dispatchable: {'yes' if response['dispatchable'] else 'no'}",
        f"- pending_operator_requests: {pending_requests}",
        (
            "- promotion_candidates: "
            f"tickets={len(promotion_candidates['tickets'])}, "
            f"chunks={len(promotion_candidates['chunks'])}, "
            f"blocks={len(promotion_candidates['blocks'])}"
        ),
        f"- sync_warnings: {len(sync_warnings)}",
        f"- advisories: {len(advisories)}",
        (
            "- close_ready_handoff: "
            f"{close_ready_handoff['next_role']} <= "
            f"{close_ready_handoff['entity_type']} {close_ready_handoff['entity_id']}"
            if close_ready_handoff["triggered"]
            else "- close_ready_handoff: inactive"
        ),
        (
            "- bounded_multi_step: "
            f"{bounded_multi_step['execution_level']} / "
            f"{'same_block + block_only_handoff' if bounded_multi_step['high_cross_block_handoff_allowed'] else 'same_block_only'} / "
            f"max_steps={bounded_multi_step['max_steps_per_run']}"
        ),
        "- limited_status_sync: pending_to_in_progress_only",
        (
            "- supplemental_canvas_sync: "
            f"{'recommended' if limited_actions['canvas_sync']['recommended'] else 'available'}"
            if limited_actions["canvas_sync"]["available"]
            else "- supplemental_canvas_sync: unavailable"
        ),
    ]
    if stop_reason and summary_next_role != route_hint:
        lines.append(f"- route_hint: {route_hint} (hard stop が無ければ)")

    if stop_reason:
        lines.append("## Stop Reason")
        lines.append(f"- {stop_reason['code']}: {stop_reason['message']}")
        evidence = stop_reason.get("evidence") or {}
        if isinstance(evidence, dict):
            if stop_reason["code"] == "bundled_confirmations_detected":
                lines.append(
                    "- evidence: "
                    f"bundle={evidence.get('bundle')} / "
                    f"keys={len(evidence.get('keys', []))}"
                )
                for item in (evidence.get("candidates") or [])[:3]:
                    if isinstance(item, dict):
                        lines.append(
                            "- confirmation_candidate: "
                            f"{item.get('key')} @ {item.get('source_type')} {item.get('source_id')} "
                            f"(line {item.get('line_number')})"
                        )
            elif stop_reason["code"] == "loop_retry_detected":
                lines.append(
                    "- evidence: "
                    f"{evidence.get('runtime_state_scope', 'shared')} state で "
                    f"同一 gateway_signature が {evidence.get('observed_count')} 回連続 / "
                    f"threshold {evidence.get('threshold')}"
                )
                repeated_entities = evidence.get("repeated_entities") or []
                for item in repeated_entities[:3]:
                    if isinstance(item, dict):
                        lines.append(
                            f"- repeated_entity: {item.get('entity_type')} {item.get('entity_id')}"
                        )
                lines.append(
                    "- runtime_state_dir: "
                    f"{evidence.get('runtime_state_dir', '-')}"
                )
            elif stop_reason["code"] == "pending_operator_request":
                lines.append(
                    "- evidence: "
                    f"pending_request_ids={', '.join(evidence.get('request_ids', [])) or '-'}"
                )

    if pending_requests:
        lines.append("## Pending Requests")
        for item in response["operator_requests"]["pending_items"][:3]:
            lines.append(f"- {item['request_id']}: {item['summary'] or '(summary なし)'}")

    if promotion_candidates["chunks"] or promotion_candidates["blocks"] or promotion_candidates["tickets"]:
        lines.append("## Promotion Candidates")
        for group_name in ("tickets", "chunks", "blocks"):
            for item in promotion_candidates[group_name][:3]:
                lines.append(f"- {item['entity_id']}: {item['reason']}")

    if sync_warnings:
        lines.append("## Sync Warnings")
        for item in sync_warnings[:5]:
            lines.append(f"- {item['entity_id']}: {item['message']}")

    if advisories:
        lines.append("## Advisories")
        for item in advisories[:5]:
            lines.append(
                "- "
                f"{item['target_role']} -> {item['followup_role']}: "
                f"{item['entity_id']} / {item['message']}"
            )

    if close_ready_handoff["triggered"]:
        lines.append("## Close-Ready Handoff")
        lines.append(
            "- "
            f"{close_ready_handoff['entity_type']} {close_ready_handoff['entity_id']}: "
            f"{close_ready_handoff['reason']}"
        )

    if high_cross_block_handoff["triggered"]:
        lines.append("## Block-Only Handoff")
        lines.append(
            "- "
            f"{high_cross_block_handoff['entity_type']} {high_cross_block_handoff['entity_id']}: "
            f"{high_cross_block_handoff['reason']}"
        )

    if reviewer_pass_through["triggered"] or reviewer_pass_through["blocking"]:
        lines.append("## Reviewer Pass-Through")
        lines.append(
            "- "
            f"{reviewer_pass_through['entity_type']} {reviewer_pass_through['entity_id']}: "
            f"{reviewer_pass_through['reason']}"
        )

    if limited_actions["canvas_sync"]["available"]:
        lines.append("## Limited Actions")
        lines.append(
            "- canvas_sync: 明示 opt-in のときだけ補助的に実行する。"
        )
        lines.append(
            "- status_sync: `pending -> in_progress` 系の機械同期だけを将来許容し、"
            " `done` 昇格や意味変更は扱わない。"
        )

    lines.append("## Bounded Multi-Step")
    lines.append(
        "- execution_level: "
        f"{bounded_multi_step['execution_level']} "
        f"(default {bounded_multi_step['default_execution_level']})"
    )
    lines.append(
        "- allowed_roles: "
        + ", ".join(bounded_multi_step["allowed_roles"])
    )
    lines.append(
        "- return_boundaries: "
        "plan_manager / reviewer_pass_through_blocking / max_steps_reached / active_block_changed"
    )
    if bounded_multi_step["high_cross_block_handoff_allowed"]:
        lines.append(
            "- block_only_handoff: "
            "LEVEL=MID 以上では block-only 状態から task_planner へ 1 段返せる"
        )

    return "\n".join(lines)


def build_runtime_response(args: ConductorArgs) -> dict[str, object]:
    plan_meta, blocks = parse_plan_spec(args.plan_spec)
    fact_report_dir = args.plan_spec.parent / "fact-reports"
    block_notes = load_dir_states(args.block_dir, parse_block_note)
    chunks = load_dir_states(args.chunk_dir, parse_chunk_states)
    tickets = load_dir_states(
        args.ticket_dir,
        lambda path: parse_ticket_states(path, fact_report_dir),
    )
    operator_requests = load_dir_states(
        args.operator_request_dir,
        parse_operator_request,
    )
    pending_requests = [item for item in operator_requests if item.status == "pending"]
    table_frontmatter_mismatches = detect_block_note_mismatches(blocks, block_notes)
    table_frontmatter_mismatches.extend(detect_chunk_table_mismatches(chunks, tickets))
    promotion_candidates = build_promotion_candidates(blocks, block_notes, chunks, tickets)
    close_ready_handoff = build_close_ready_handoff(
        args, blocks, block_notes, chunks, tickets
    )
    high_cross_block_handoff = build_high_cross_block_handoff(
        args,
        blocks,
        chunks,
        tickets,
    )
    reviewer_pass_through = build_reviewer_pass_through(tickets)
    sync_warnings = build_sync_warnings(
        blocks,
        chunks,
        tickets,
        table_frontmatter_mismatches,
    )
    route_hint = infer_route_hint(
        pending_requests,
        tickets,
        chunks,
        promotion_candidates,
        sync_warnings,
        close_ready_handoff,
        high_cross_block_handoff,
        reviewer_pass_through,
    )
    advisories = build_advisories(
        route_hint,
        promotion_candidates,
        sync_warnings,
    )
    confirmation_candidates = collect_confirmation_candidates(
        blocks,
        block_notes,
        chunks,
        tickets,
        pending_requests,
    )
    gateway_signature = build_gateway_signature(
        route_hint,
        blocks,
        chunks,
        tickets,
        pending_requests,
        advisories,
        promotion_candidates,
    )
    observation = observe_gateway_signature(
        args.runtime_state_dir,
        args.plan_spec,
        gateway_signature,
    )
    loop_stop_reason = build_loop_stop_reason(
        route_hint,
        blocks,
        chunks,
        tickets,
        observation,
    )
    bundled_confirmation_stop_reason = build_bundled_confirmation_stop_reason(
        confirmation_candidates
    )
    stop_reason = build_stop_reason(
        pending_requests,
        bundled_confirmation_stop_reason,
        loop_stop_reason,
    )
    bounded_multi_step = build_bounded_multi_step_state(
        route_hint,
        stop_reason,
        blocks,
        args,
        high_cross_block_handoff,
    )
    limited_actions = build_limited_actions(stop_reason, advisories)
    dispatchable = infer_dispatchable(route_hint, stop_reason)
    return {
        "status": "ok",
        "mode": "runtime_state",
        "gateway_mode": "post_role",
        "plan": {
            "plan_id": plan_meta["plan_id"],
            "status": plan_meta.get("status", ""),
            "source_path": str(args.plan_spec),
        },
        "paths": {
            "plan_spec": path_payload(args.plan_spec),
            "block_dir": path_payload(args.block_dir),
            "chunk_dir": path_payload(args.chunk_dir),
            "ticket_dir": path_payload(args.ticket_dir),
            "operator_request_dir": path_payload(args.operator_request_dir),
            "runtime_state_dir": path_payload(args.runtime_state_dir),
        },
        "current_state": {
            "counts": {
                "blocks": summarize_status(blocks),
                "chunks": summarize_status(chunks),
                "tickets": summarize_status(tickets),
                "operator_requests": summarize_status(operator_requests),
            },
            "active_blocks": [asdict(item) for item in blocks if item.status == "in_progress"],
            "active_chunks": [asdict(item) for item in chunks if item.status == "in_progress"],
            "active_tickets": [asdict(item) for item in tickets if item.status == "in_progress"],
            "pending_tickets": [asdict(item) for item in tickets if item.status == "pending"],
        },
        "operator_requests": {
            "pending_count": len(pending_requests),
            "pending_items": [asdict(item) for item in pending_requests],
        },
        "promotion_candidates": promotion_candidates,
        "close_ready_handoff": close_ready_handoff,
        "high_cross_block_handoff": high_cross_block_handoff,
        "reviewer_pass_through": reviewer_pass_through,
        "confirmation_candidates": confirmation_candidates,
        "sync_warnings": sync_warnings,
        "advisories": advisories,
        "table_frontmatter_mismatches": table_frontmatter_mismatches,
        "gateway_signature": gateway_signature,
        "runtime_observation": observation,
        "bounded_multi_step": bounded_multi_step,
        "route_hint": route_hint,
        "dispatchable": dispatchable,
        "stop_reason": stop_reason,
        "limited_actions": limited_actions,
    }


def build_scaffold_response(args: ConductorArgs) -> dict[str, object]:
    return {
        "status": "ok",
        "mode": "scaffold",
        "message": "runtime state parsing は未実装です。次の実装ステップで追加してください。",
        "paths": {
            "plan_spec": path_payload(args.plan_spec),
            "block_dir": path_payload(args.block_dir),
            "chunk_dir": path_payload(args.chunk_dir),
            "ticket_dir": path_payload(args.ticket_dir),
            "operator_request_dir": path_payload(args.operator_request_dir),
        },
        "next_ticket": None,
        "route_hint": "task_worker",
        "args": {key: str(value) for key, value in asdict(args).items()},
    }


def main() -> int:
    try:
        args = parse_args()
        validate_args(args)
        response = build_runtime_response(args)
        if args.human:
            print(build_human_summary(response), file=sys.stderr)
        print(json.dumps(response, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001 - keep scaffold failure handling simple
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": str(exc),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
