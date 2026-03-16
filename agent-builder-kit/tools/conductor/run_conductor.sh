#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "$SCRIPT_DIR/../../docs" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi
CONDUCTOR_SCRIPT="$SCRIPT_DIR/flow_conductor.py"
CANVAS_SYNC_SCRIPT="$REPO_ROOT/tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PLAN_SPEC_PATH="$REPO_ROOT/docs/exec-plans/plan-spec.md"
BLOCK_DIR_PATH="$REPO_ROOT/docs/exec-plans/blocks"
CHUNK_DIR_PATH="$REPO_ROOT/docs/exec-plans/chunks"
TICKET_DIR_PATH="$REPO_ROOT/docs/exec-plans/tickets"
OPERATOR_REQUEST_DIR_PATH="$REPO_ROOT/docs/exec-plans/operator-requests"

usage() {
  cat <<'EOF'
Usage:
  run_conductor.sh [options]

Options:
  --human                     人間向け summary を stderr に出す
  --plan-spec <path>          plan-spec path
  --block-dir <path>          block directory path
  --chunk-dir <path>          chunk directory path
  --ticket-dir <path>         ticket directory path
  --operator-request-dir <path>
                              operator request directory path
  --runtime-state-dir <path>  loop 判定用 runtime state directory path
  --level <MID|HIGH>          execution level override
  --max-steps <num>           same-block bounded run の最大 step 数 override
  --sync-canvas               明示 opt-in で補助 `.canvas` sync を実行
  -h, --help                  この help を表示

Exit codes:
  0   正常終了。hard stop なし
  20  hard stop あり
  1   実行失敗
EOF
}

if [[ ! -f "$CONDUCTOR_SCRIPT" ]]; then
  echo "Conductor script is missing: $CONDUCTOR_SCRIPT" >&2
  exit 1
fi

HUMAN=0
SYNC_CANVAS=0
CONDUCTOR_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --human)
      HUMAN=1
      CONDUCTOR_ARGS+=("$1")
      shift
      ;;
    --sync-canvas)
      SYNC_CANVAS=1
      shift
      ;;
    --plan-spec|--block-dir|--chunk-dir|--ticket-dir|--operator-request-dir|--runtime-state-dir|--level|--max-steps)
      option="$1"
      value="${2:?missing value for $1}"
      case "$option" in
        --plan-spec)
          PLAN_SPEC_PATH="$value"
          ;;
        --block-dir)
          BLOCK_DIR_PATH="$value"
          ;;
        --chunk-dir)
          CHUNK_DIR_PATH="$value"
          ;;
        --ticket-dir)
          TICKET_DIR_PATH="$value"
          ;;
        --operator-request-dir)
          OPERATOR_REQUEST_DIR_PATH="$value"
          ;;
      esac
      CONDUCTOR_ARGS+=("$option" "$value")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

json_output="$("$PYTHON_BIN" "$CONDUCTOR_SCRIPT" "${CONDUCTOR_ARGS[@]}")"
printf '%s\n' "$json_output"

pending_count="$(
  JSON_PAYLOAD="$json_output" "$PYTHON_BIN" - <<'PY'
import json
import os

payload = json.loads(os.environ["JSON_PAYLOAD"])
print(payload.get("operator_requests", {}).get("pending_count", 0))
PY
)"

stop_reason_code="$(
  JSON_PAYLOAD="$json_output" "$PYTHON_BIN" - <<'PY'
import json
import os

payload = json.loads(os.environ["JSON_PAYLOAD"])
stop_reason = payload.get("stop_reason") or {}
print(stop_reason.get("code", ""))
PY
)"

wrapper_note="$(
  JSON_PAYLOAD="$json_output" "$PYTHON_BIN" - <<'PY'
import json
import os

payload = json.loads(os.environ["JSON_PAYLOAD"])
stop_reason = payload.get("stop_reason") or {}
advisories = payload.get("advisories", [])
close_ready_handoff = payload.get("close_ready_handoff") or {}
high_cross_block_handoff = payload.get("high_cross_block_handoff") or {}
reviewer_pass_through = payload.get("reviewer_pass_through") or {}
bounded_multi_step = payload.get("bounded_multi_step") or {}
code = stop_reason.get("code", "")

def display_role(value: str) -> str:
    return value.replace("_", "-")

if code == "pending_operator_request":
    next_role = display_role(stop_reason.get("next_role", "task_planner"))
    print(
        "pending operator request があるため、自動続行せず "
        f"{next_role} へ戻してください。"
    )
elif code == "bundled_confirmations_detected":
    evidence = stop_reason.get("evidence") or {}
    bundle = evidence.get("bundle", "?")
    key_count = len(evidence.get("keys") or [])
    candidates = evidence.get("candidates") or []
    if candidates:
        focus = candidates[0]
        focus_label = f"{focus.get('source_type', 'note')} {focus.get('source_id', '?')}"
    else:
        focus_label = "active note"
    next_role = display_role(stop_reason.get("next_role", "plan_manager"))
    print(
        f"bundle {bundle} に独立 confirmation key が {key_count} 件あるため、"
        f"{focus_label} を起点に自動続行せず {next_role} へ戻してください。"
    )
elif code == "loop_retry_detected":
    evidence = stop_reason.get("evidence") or {}
    observed_count = evidence.get("observed_count", "?")
    threshold = evidence.get("threshold", "?")
    runtime_state_scope = evidence.get("runtime_state_scope", "shared")
    repeated_entities = evidence.get("repeated_entities") or []
    if repeated_entities:
        focus = repeated_entities[0]
        label = f"{focus.get('entity_type', 'entity')} {focus.get('entity_id', '')}".strip()
    else:
        label = "同一論点"
    next_role = display_role(stop_reason.get("next_role", "task_planner"))
    print(
        f"{runtime_state_scope} state で {label} を含む同一 gateway_signature が "
        f"{observed_count} 回連続 (threshold {threshold}) で観測されたため、"
        f"自動続行せず {next_role} へ戻してください。"
    )
elif code:
    print(f"stop_reason={code} のため、自動続行を止めました。")
elif reviewer_pass_through.get("triggered"):
    print(
        f"reviewer pass-through により "
        f"{reviewer_pass_through.get('entity_type', 'ticket')} "
        f"{reviewer_pass_through.get('entity_id', '')} で "
        "internal reviewer を先に通します。"
    )
elif reviewer_pass_through.get("blocking"):
    print(
        f"reviewer finding が残っているため "
        f"{reviewer_pass_through.get('entity_type', 'ticket')} "
        f"{reviewer_pass_through.get('entity_id', '')} を task-worker へ戻してください。"
    )
elif close_ready_handoff.get("triggered"):
    next_role = display_role(close_ready_handoff.get("next_role", "task_planner"))
    print(
        f"close-ready handoff により "
        f"{close_ready_handoff.get('entity_type', 'frontier')} "
        f"{close_ready_handoff.get('entity_id', '')} を "
        f"{next_role} へ返します。"
    )
elif high_cross_block_handoff.get("triggered"):
    level = bounded_multi_step.get("execution_level", "MID")
    print(
        f"LEVEL={level} の block-only handoff により "
        f"{high_cross_block_handoff.get('entity_type', 'frontier')} "
        f"{high_cross_block_handoff.get('entity_id', '')} を "
        "task-planner へ返します。"
    )
elif advisories:
    print("advisory があります。現在の role は継続できますが、区切りで task-planner へ共有してください。")
else:
    bounded = payload.get("bounded_multi_step") or {}
    if bounded.get("enabled"):
        max_steps = bounded.get("max_steps_per_run", "?")
        level = bounded.get("execution_level", "MID")
        extra = ""
        if bounded.get("high_cross_block_handoff_allowed"):
            extra = "MID 以上では block-only 状態から task-planner への 1 段 handoff も許します。"
        print(
            f"LEVEL={level} の bounded auto として "
            f"task-worker / task-planner を最大 {max_steps} step まで継続できます。"
            f"{extra}"
            "plan-manager、reviewer handoff、hard stop、step 上限で停止します。"
        )
PY
)"

if [[ "$HUMAN" -eq 1 && -n "$wrapper_note" ]]; then
  echo "wrapper_note=$wrapper_note" >&2
fi

PLANNING_ROOT="$(dirname "$PLAN_SPEC_PATH")"
DOCS_ROOT="$(dirname "$PLANNING_ROOT")"
REFERENCE_DIR_PATH="$DOCS_ROOT/references"
CANVAS_PATH="$PLANNING_ROOT/canvas/development-flow.canvas"

if [[ "$SYNC_CANVAS" -eq 1 ]]; then
  if [[ -n "$stop_reason_code" ]]; then
    if [[ "$HUMAN" -eq 1 ]]; then
      echo "wrapper_note=hard stop があるため、補助 .canvas sync は実行しませんでした。" >&2
    fi
  elif [[ ! -f "$CANVAS_SYNC_SCRIPT" ]]; then
    echo "Conductor canvas sync script is missing: $CANVAS_SYNC_SCRIPT" >&2
    exit 1
  else
    "$PYTHON_BIN" "$CANVAS_SYNC_SCRIPT" \
      --plan-spec "$PLAN_SPEC_PATH" \
      --block-dir "$BLOCK_DIR_PATH" \
      --chunk-dir "$CHUNK_DIR_PATH" \
      --ticket-dir "$TICKET_DIR_PATH" \
      --reference-dir "$REFERENCE_DIR_PATH" \
      --canvas "$CANVAS_PATH" \
      --vault-root "$REPO_ROOT" >&2
    if [[ "$HUMAN" -eq 1 ]]; then
      echo "wrapper_note=補助 .canvas sync を実行しました。source docs の正本性は各 role 側に残ります。" >&2
    fi
  fi
fi

if [[ "$pending_count" != "0" || -n "$stop_reason_code" ]]; then
  exit 20
fi

exit 0
