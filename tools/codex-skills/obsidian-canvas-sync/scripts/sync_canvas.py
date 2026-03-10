#!/usr/bin/env python3
"""Deterministically generate or update an Obsidian .canvas from planning docs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


MANAGED_NODE_PREFIX = "flow:"
MANAGED_EDGE_PREFIX = "flow-edge:"
BLOCK_SECTION = "High-level blocks"
CHUNK_TICKET_SECTION = "含む ticket"
A_X = 0
B_X = 620
C_X = 1240
DEFAULT_MANUAL_LANE_X = 3600
REFERENCE_Y = -280
REFERENCE_WIDTH = 280
REFERENCE_HEIGHT = 140
REFERENCE_GAP = 40
TOP_MARGIN = 120
BLOCK_GAP = 120
ROW_GAP = 48
BLOCK_WIDTH = 420
CHUNK_WIDTH = 420
TICKET_WIDTH = 280
ROW_HEIGHT = 160
TICKET_GAP = 40
EDGE_COLOR = "#94A3B8"
REFERENCE_COLOR = "#475569"
STATUS_COLORS = {
    "pending": "#000000",
    "in_progress": "#10B981",
    "done": "#FFFFFF",
    "blocked": "#B91C1C",
    "obsolete": "#94A3B8",
}
META_RE = re.compile(r"^-\s+([A-Za-z0-9_-]+):\s*(.+?)\s*$")
FRONTMATTER_BOUNDARY = "---"


@dataclass
class CanvasArgs:
    plan_spec: Path
    block_dir: Path | None
    chunk_dir: Path | None
    ticket_dir: Path | None
    reference_dir: Path | None
    canvas: Path
    manual_lane_x: int
    vault_root: Path | None


@dataclass
class Block:
    block_id: str
    title: str
    goal: str
    status: str
    depends_on: str = "-"
    source_path: str | None = None


@dataclass
class Ticket:
    ticket_id: str
    parent_chunk: str
    title: str
    status: str
    lane_order: int = 100
    source_path: str | None = None


@dataclass
class Chunk:
    chunk_id: str
    parent_block: str
    title: str
    status: str
    source_path: str | None = None
    ticket_stubs: list[Ticket] = field(default_factory=list)


@dataclass
class LayoutRow:
    chunk: Chunk | None
    tickets: list[Ticket]
    y: int
    height: int


@dataclass
class ReferenceNote:
    reference_id: str
    title: str
    lane_order: int = 100
    source_path: str | None = None


def parse_args() -> CanvasArgs:
    parser = argparse.ArgumentParser(
        description="Generate or update an Obsidian .canvas from plan/chunk/ticket docs."
    )
    parser.add_argument("--plan-spec", required=True, type=Path)
    parser.add_argument("--block-dir", type=Path)
    parser.add_argument("--chunk-dir", type=Path)
    parser.add_argument("--ticket-dir", type=Path)
    parser.add_argument("--reference-dir", type=Path)
    parser.add_argument("--canvas", required=True, type=Path)
    parser.add_argument("--manual-lane-x", type=int, default=DEFAULT_MANUAL_LANE_X)
    parser.add_argument("--vault-root", type=Path)
    ns = parser.parse_args()
    return CanvasArgs(
        plan_spec=ns.plan_spec,
        block_dir=ns.block_dir,
        chunk_dir=ns.chunk_dir,
        ticket_dir=ns.ticket_dir,
        reference_dir=ns.reference_dir,
        canvas=ns.canvas,
        manual_lane_x=ns.manual_lane_x,
        vault_root=ns.vault_root,
    )


def read_markdown(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def first_heading(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def parse_metadata(lines: list[str]) -> dict[str, str]:
    data = parse_frontmatter(lines)
    if data:
        return data
    data = {}
    for line in lines:
        match = META_RE.match(line.strip())
        if match:
            data[match.group(1)] = match.group(2)
    return data


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


def parse_markdown_table(lines: list[str]) -> list[dict[str, str]]:
    if len(lines) < 2:
        return []
    headers = split_table_row(lines[0])
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        if not line.strip():
            continue
        cells = split_table_row(line)
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append({header: cells[idx] for idx, header in enumerate(headers)})
    return rows


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_plan_spec(path: Path) -> list[Block]:
    rows = extract_table(read_markdown(path), BLOCK_SECTION)
    blocks: list[Block] = []
    for row in rows:
        block_id = row.get("block_id", "").strip()
        if not block_id:
            continue
        blocks.append(
            Block(
                block_id=block_id,
                title=row.get("title", "").strip() or block_id,
                goal=row.get("goal", "").strip(),
                status=normalize_status(row.get("status", "")),
                depends_on=row.get("depends_on", "").strip() or "-",
            )
        )
    return blocks


def attach_block_sources(blocks: list[Block], block_dir: Path | None) -> None:
    if block_dir is None or not block_dir.exists():
        return
    block_files: dict[str, str] = {}
    for path in sorted(block_dir.rglob("*.md")):
        metadata = parse_metadata(read_markdown(path))
        block_id = metadata.get("block_id", "").strip()
        if block_id:
            block_files[block_id] = str(path)
    for block in blocks:
        block.source_path = block_files.get(block.block_id)


def parse_chunks(chunk_dir: Path | None) -> list[Chunk]:
    if chunk_dir is None or not chunk_dir.exists():
        return []
    chunks: list[Chunk] = []
    for path in sorted(chunk_dir.rglob("*.md")):
        lines = read_markdown(path)
        metadata = parse_metadata(lines)
        chunk_id = metadata.get("chunk_id", "").strip()
        if not chunk_id:
            continue
        chunk = Chunk(
            chunk_id=chunk_id,
            parent_block=metadata.get("parent_block", "").strip(),
            title=metadata.get("title", "").strip() or first_heading(lines) or chunk_id,
            status=normalize_status(metadata.get("status", "")),
            source_path=str(path),
            ticket_stubs=parse_chunk_ticket_stubs(lines, chunk_id, path),
        )
        chunks.append(chunk)
    return chunks


def parse_chunk_ticket_stubs(
    lines: list[str], chunk_id: str, path: Path
) -> list[Ticket]:
    rows = extract_table(lines, CHUNK_TICKET_SECTION)
    tickets: list[Ticket] = []
    for order, row in enumerate(rows):
        ticket_id = row.get("ticket_id", "").strip()
        if not ticket_id:
            continue
        title = row.get("title", "").strip() or ticket_id
        status = normalize_status(row.get("status", "pending"))
        tickets.append(
            Ticket(
                ticket_id=ticket_id,
                parent_chunk=chunk_id,
                title=title,
                status=status,
                lane_order=(order + 1) * 100,
                source_path=str(path),
            )
        )
    return tickets


def parse_tickets(ticket_dir: Path | None) -> list[Ticket]:
    if ticket_dir is None or not ticket_dir.exists():
        return []
    tickets: list[Ticket] = []
    for path in sorted(ticket_dir.rglob("*.md")):
        lines = read_markdown(path)
        metadata = parse_metadata(lines)
        ticket_id = metadata.get("ticket_id", "").strip()
        if not ticket_id:
            continue
        tickets.append(
            Ticket(
                ticket_id=ticket_id,
                parent_chunk=metadata.get("parent_chunk", "").strip(),
                title=metadata.get("title", "").strip() or first_heading(lines) or ticket_id,
                status=normalize_status(metadata.get("status", "")),
                lane_order=parse_int(metadata.get("lane_order", ""), 100),
                source_path=str(path),
            )
        )
    return tickets


def parse_references(reference_dir: Path | None) -> list[ReferenceNote]:
    if reference_dir is None or not reference_dir.exists():
        return []
    references: list[ReferenceNote] = []
    for path in sorted(reference_dir.rglob("*.md")):
        lines = read_markdown(path)
        metadata = parse_metadata(lines)
        reference_id = metadata.get("reference_id", "").strip()
        if not reference_id:
            continue
        references.append(
            ReferenceNote(
                reference_id=reference_id,
                title=metadata.get("title", "").strip() or first_heading(lines) or reference_id,
                lane_order=parse_int(metadata.get("lane_order", ""), 100),
                source_path=str(path),
            )
        )
    return sorted(references, key=lambda item: (item.lane_order, item.reference_id))


def normalize_status(value: str) -> str:
    candidate = value.strip().lower().replace(" ", "_")
    return candidate if candidate in STATUS_COLORS else "pending"


def parse_int(value: str, default: int) -> int:
    try:
        return int(value.strip())
    except (TypeError, ValueError, AttributeError):
        return default


def merge_tickets(chunks: list[Chunk], ticket_docs: list[Ticket]) -> dict[str, list[Ticket]]:
    by_chunk: dict[str, list[Ticket]] = {}
    for chunk in chunks:
        by_chunk[chunk.chunk_id] = list(chunk.ticket_stubs)
    if not ticket_docs:
        for chunk_id in by_chunk:
            by_chunk[chunk_id] = sorted(
                by_chunk[chunk_id], key=lambda item: (item.lane_order, item.ticket_id)
            )
        return by_chunk
    by_id = {ticket.ticket_id: ticket for ticket in ticket_docs}
    for chunk_id, stubs in by_chunk.items():
        merged: list[Ticket] = []
        seen_ids: set[str] = set()
        for stub in stubs:
            doc = by_id.get(stub.ticket_id)
            merged.append(doc if doc is not None else stub)
            seen_ids.add(stub.ticket_id)
        for ticket in ticket_docs:
            if ticket.parent_chunk == chunk_id and ticket.ticket_id not in seen_ids:
                merged.append(ticket)
        by_chunk[chunk_id] = sorted(merged, key=lambda item: (item.lane_order, item.ticket_id))
    for ticket in ticket_docs:
        if ticket.parent_chunk and ticket.parent_chunk not in by_chunk:
            by_chunk[ticket.parent_chunk] = [ticket]
    return by_chunk


def build_layout_rows(
    blocks: list[Block],
    chunks: list[Chunk],
    tickets_by_chunk: dict[str, list[Ticket]],
    references: list[ReferenceNote],
    vault_root: Path | None,
) -> tuple[list[dict], list[dict], int]:
    chunks_by_block: dict[str, list[Chunk]] = {}
    for chunk in chunks:
        chunks_by_block.setdefault(chunk.parent_block, []).append(chunk)
    for block_chunks in chunks_by_block.values():
        block_chunks.sort(key=lambda item: item.chunk_id)

    nodes: list[dict] = build_reference_band(references, vault_root)
    edges: list[dict] = []
    current_y = TOP_MARGIN
    max_ticket_count = 1
    previous_block_id: str | None = None

    for block in blocks:
        current_block_node_id = block_node_id(block.block_id)
        block_chunks = chunks_by_block.get(block.block_id, [])
        rows: list[LayoutRow] = []
        if block_chunks:
            for index, chunk in enumerate(block_chunks):
                row_y = current_y + index * (ROW_HEIGHT + ROW_GAP)
                chunk_tickets = tickets_by_chunk.get(chunk.chunk_id, [])
                max_ticket_count = max(max_ticket_count, len(chunk_tickets) or 1)
                rows.append(LayoutRow(chunk=chunk, tickets=chunk_tickets, y=row_y, height=ROW_HEIGHT))
        else:
            rows.append(LayoutRow(chunk=None, tickets=[], y=current_y, height=ROW_HEIGHT))

        block_height = len(rows) * ROW_HEIGHT + max(len(rows) - 1, 0) * ROW_GAP
        nodes.append(
            make_node(
                node_id=current_block_node_id,
                x=A_X,
                y=current_y,
                width=BLOCK_WIDTH,
                height=block_height,
                text=format_block_text(block, vault_root),
                color=status_color(block.status),
                source_path=block.source_path,
                vault_root=vault_root,
            )
        )

        if previous_block_id is not None:
            edges.append(
                make_edge(
                    edge_id=edge_id(block_node_id(previous_block_id), current_block_node_id),
                    from_node=block_node_id(previous_block_id),
                    to_node=current_block_node_id,
                    from_side="bottom",
                    to_side="top",
                )
            )

        previous_chunk_node_id: str | None = None
        first_chunk_node_id: str | None = None

        for row in rows:
            if row.chunk is None:
                continue
            current_chunk_node_id = chunk_node_id(row.chunk.chunk_id)
            nodes.append(
                make_node(
                    node_id=current_chunk_node_id,
                    x=B_X,
                    y=row.y,
                    width=CHUNK_WIDTH,
                    height=row.height,
                    text=format_chunk_text(row.chunk, len(row.tickets), vault_root),
                    color=status_color(row.chunk.status),
                    source_path=row.chunk.source_path,
                    vault_root=vault_root,
                )
            )
            if first_chunk_node_id is None:
                first_chunk_node_id = current_chunk_node_id
            if previous_chunk_node_id is not None:
                edges.append(
                    make_edge(
                        edge_id=edge_id(previous_chunk_node_id, current_chunk_node_id),
                        from_node=previous_chunk_node_id,
                        to_node=current_chunk_node_id,
                        from_side="bottom",
                        to_side="top",
                    )
                )
            previous_chunk_node_id = current_chunk_node_id

            for index, ticket in enumerate(row.tickets):
                ticket_x = C_X + index * (TICKET_WIDTH + TICKET_GAP)
                nodes.append(
                    make_node(
                        node_id=ticket_node_id(ticket.ticket_id),
                        x=ticket_x,
                        y=row.y,
                        width=TICKET_WIDTH,
                        height=row.height,
                        text=format_ticket_text(ticket, vault_root),
                        color=status_color(ticket.status),
                        source_path=ticket.source_path,
                        vault_root=vault_root,
                    )
                )
                edges.append(
                    make_edge(
                        edge_id=edge_id(current_chunk_node_id, ticket_node_id(ticket.ticket_id)),
                        from_node=current_chunk_node_id,
                        to_node=ticket_node_id(ticket.ticket_id),
                    )
                )

        if first_chunk_node_id is not None:
            edges.append(
                make_edge(
                    edge_id=edge_id(current_block_node_id, first_chunk_node_id),
                    from_node=current_block_node_id,
                    to_node=first_chunk_node_id,
                )
            )

        current_y += block_height + BLOCK_GAP
        previous_block_id = block.block_id

    effective_manual_lane_x = max(
        DEFAULT_MANUAL_LANE_X,
        C_X + max_ticket_count * (TICKET_WIDTH + TICKET_GAP) + 320,
    )
    return nodes, edges, effective_manual_lane_x


def build_reference_band(references: list[ReferenceNote], vault_root: Path | None) -> list[dict]:
    if not references:
        return []
    band_center = (B_X + C_X + REFERENCE_WIDTH) // 2
    band_width = len(references) * REFERENCE_WIDTH + max(len(references) - 1, 0) * REFERENCE_GAP
    start_x = band_center - band_width // 2
    nodes: list[dict] = []
    for index, reference in enumerate(references):
        nodes.append(
            make_node(
                node_id=reference_node_id(reference.reference_id),
                x=start_x + index * (REFERENCE_WIDTH + REFERENCE_GAP),
                y=REFERENCE_Y,
                width=REFERENCE_WIDTH,
                height=REFERENCE_HEIGHT,
                text=format_reference_text(reference, vault_root),
                color=REFERENCE_COLOR,
                source_path=reference.source_path,
                vault_root=vault_root,
            )
        )
    return nodes


def make_node(
    node_id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    text: str,
    color: str,
    source_path: str | None,
    vault_root: Path | None,
) -> dict:
    return {
        "id": node_id,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "text": build_link_text(text, source_path, vault_root),
        "color": color,
    }


def make_edge(
    edge_id: str,
    from_node: str,
    to_node: str,
    from_side: str = "right",
    to_side: str = "left",
) -> dict:
    return {
        "id": edge_id,
        "fromNode": from_node,
        "fromSide": from_side,
        "toNode": to_node,
        "toSide": to_side,
        "color": EDGE_COLOR,
    }


def status_color(status: str) -> str:
    return STATUS_COLORS.get(status, STATUS_COLORS["pending"])


def block_node_id(block_id: str) -> str:
    return f"{MANAGED_NODE_PREFIX}block:{block_id}"


def chunk_node_id(chunk_id: str) -> str:
    return f"{MANAGED_NODE_PREFIX}chunk:{chunk_id}"


def ticket_node_id(ticket_id: str) -> str:
    return f"{MANAGED_NODE_PREFIX}ticket:{ticket_id}"


def reference_node_id(reference_id: str) -> str:
    return f"{MANAGED_NODE_PREFIX}ref:{reference_id}"


def edge_id(from_node: str, to_node: str) -> str:
    return f"{MANAGED_EDGE_PREFIX}{from_node}->{to_node}"


def format_block_text(block: Block, vault_root: Path | None) -> str:
    goal = f"\n\n{block.goal}" if block.goal else ""
    return f"# {block.title}\n`{block.block_id}`\nstatus: `{block.status}`{goal}"


def format_chunk_text(chunk: Chunk, ticket_count: int, vault_root: Path | None) -> str:
    return (
        f"## {chunk.title}\n"
        f"`{chunk.chunk_id}`\n"
        f"status: `{chunk.status}`\n"
        f"tickets: `{ticket_count}`"
    )


def format_ticket_text(ticket: Ticket, vault_root: Path | None) -> str:
    return f"### {ticket.title}\n`{ticket.ticket_id}`\nstatus: `{ticket.status}`"


def format_reference_text(reference: ReferenceNote, vault_root: Path | None) -> str:
    return f"## {reference.title}\n`{reference.reference_id}`\nreference"


def build_link_text(text: str, source_path: str | None, vault_root: Path | None) -> str:
    if not source_path or vault_root is None:
        return text
    source = Path(source_path)
    try:
        relative = source.resolve().relative_to(vault_root.resolve()).as_posix()
    except ValueError:
        relative = source.as_posix()
    lines = text.splitlines()
    if not lines:
        return f"[open]({relative})"
    first = lines[0]
    if first.startswith("### "):
        lines[0] = f"### [{first[4:]}]({relative})"
    elif first.startswith("## "):
        lines[0] = f"## [{first[3:]}]({relative})"
    elif first.startswith("# "):
        lines[0] = f"# [{first[2:]}]({relative})"
    else:
        lines.insert(0, f"[open]({relative})")
    return "\n".join(lines)


def load_existing_canvas(path: Path) -> dict:
    if not path.exists():
        return {"nodes": [], "edges": []}
    return json.loads(path.read_text(encoding="utf-8"))


def is_managed_node_id(node_id: str) -> bool:
    return node_id.startswith(MANAGED_NODE_PREFIX)


def is_managed_edge_id(edge_id_value: str) -> bool:
    return edge_id_value.startswith(MANAGED_EDGE_PREFIX)


def split_existing_canvas(existing: dict, manual_lane_x: int) -> tuple[list[dict], list[dict]]:
    preserved_nodes: list[dict] = []
    preserved_ids: set[str] = set()
    for node in existing.get("nodes", []):
        node_id = node.get("id", "")
        if is_managed_node_id(node_id):
            continue
        preserved = dict(node)
        if int(preserved.get("x", manual_lane_x)) < manual_lane_x:
            preserved["x"] = manual_lane_x
        preserved_nodes.append(preserved)
        preserved_ids.add(node_id)

    preserved_edges: list[dict] = []
    for edge in existing.get("edges", []):
        edge_id_value = edge.get("id", "")
        if is_managed_edge_id(edge_id_value):
            continue
        from_node = edge.get("fromNode", "")
        to_node = edge.get("toNode", "")
        if from_node in preserved_ids and to_node in preserved_ids:
            preserved_edges.append(dict(edge))
    return preserved_nodes, preserved_edges


def compose_canvas(
    existing: dict, managed_nodes: list[dict], managed_edges: list[dict], manual_lane_x: int
) -> dict:
    preserved_nodes, preserved_edges = split_existing_canvas(existing, manual_lane_x)
    nodes = sorted(preserved_nodes + managed_nodes, key=lambda item: (item["y"], item["x"], item["id"]))
    edges = preserved_edges + managed_edges
    return {"nodes": nodes, "edges": edges}


def derive_vault_root(args: CanvasArgs) -> Path:
    if args.vault_root is not None:
        return args.vault_root.resolve()
    candidates = [args.plan_spec.resolve(), args.canvas.resolve().parent]
    if args.block_dir is not None:
        candidates.append(args.block_dir.resolve())
    if args.chunk_dir is not None:
        candidates.append(args.chunk_dir.resolve())
    if args.ticket_dir is not None:
        candidates.append(args.ticket_dir.resolve())
    if args.reference_dir is not None:
        candidates.append(args.reference_dir.resolve())
    shared_parts: list[str] = []
    for segment_tuple in zip(*(path.parts for path in candidates)):
        if len(set(segment_tuple)) != 1:
            break
        shared_parts.append(segment_tuple[0])
    return Path(*shared_parts) if shared_parts else args.plan_spec.resolve().parent


def validate_blocks(blocks: list[Block]) -> None:
    if not blocks:
        raise ValueError("plan-spec に 'High-level blocks' テーブルが見つかりません。")
    missing_titles = [block.block_id for block in blocks if not block.title]
    if missing_titles:
        raise ValueError(f"block title が欠けています: {', '.join(missing_titles)}")


def validate_chunks(chunks: list[Chunk], block_ids: set[str]) -> None:
    missing = [chunk.chunk_id for chunk in chunks if not chunk.parent_block]
    if missing:
        raise ValueError(f"parent_block が欠けている chunk があります: {', '.join(missing)}")
    unknown = [chunk.chunk_id for chunk in chunks if chunk.parent_block not in block_ids]
    if unknown:
        raise ValueError(
            "plan-spec に存在しない parent_block を参照する chunk があります: "
            + ", ".join(unknown)
        )


def validate_tickets(tickets_by_chunk: dict[str, list[Ticket]], chunk_ids: set[str]) -> None:
    missing = []
    for chunk_id, tickets in tickets_by_chunk.items():
        for ticket in tickets:
            if not ticket.parent_chunk:
                missing.append(f"{ticket.ticket_id} (chunk={chunk_id})")
    if missing:
        raise ValueError(f"parent_chunk が欠けている ticket があります: {', '.join(missing)}")
    unknown_chunks = [chunk_id for chunk_id in tickets_by_chunk if chunk_id not in chunk_ids]
    if unknown_chunks:
        raise ValueError(
            "chunk-sheet に存在しない parent_chunk を参照する ticket があります: "
            + ", ".join(sorted(unknown_chunks))
        )


def main() -> int:
    args = parse_args()
    blocks = parse_plan_spec(args.plan_spec)
    attach_block_sources(blocks, args.block_dir)
    chunks = parse_chunks(args.chunk_dir)
    ticket_docs = parse_tickets(args.ticket_dir)
    references = parse_references(args.reference_dir)
    tickets_by_chunk = merge_tickets(chunks, ticket_docs)
    vault_root = derive_vault_root(args)
    validate_blocks(blocks)
    validate_chunks(chunks, {block.block_id for block in blocks})
    validate_tickets(tickets_by_chunk, {chunk.chunk_id for chunk in chunks})

    managed_nodes, managed_edges, computed_manual_lane_x = build_layout_rows(
        blocks, chunks, tickets_by_chunk, references, vault_root
    )
    effective_manual_lane_x = max(args.manual_lane_x, computed_manual_lane_x)
    existing = load_existing_canvas(args.canvas)
    updated = compose_canvas(existing, managed_nodes, managed_edges, effective_manual_lane_x)

    args.canvas.parent.mkdir(parents=True, exist_ok=True)
    args.canvas.write_text(
        json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "canvas": str(args.canvas),
                "blocks": len(blocks),
                "chunks": len(chunks),
                "tickets": sum(len(items) for items in tickets_by_chunk.values()),
                "references": len(references),
                "manual_lane_x": effective_manual_lane_x,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
