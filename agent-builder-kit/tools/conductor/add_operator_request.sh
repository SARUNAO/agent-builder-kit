#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -d "$SCRIPT_DIR/../../docs" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi
DEFAULT_TEMPLATE="$REPO_ROOT/docs/templates/operator-request-template.md"
DEFAULT_REQUEST_DIR="$REPO_ROOT/docs/exec-plans/operator-requests"

usage() {
  cat <<'EOF'
Usage:
  add_operator_request.sh --summary "要望" [options]

Options:
  --summary <text>            要約。必須
  --requested-role <role>     次に見てほしい role。既定: task_planner
  --detail <text>             detail 節の本文
  --expected-handling <text>  expected_handling 節の本文
  --notes <text>              notes 節の本文
  --interrupt-mode <mode>     既定: after_current_ticket
  --requested-by <name>       既定: human_operator
  --target-scope <text>       既定: -
  --related-ref <path>        related_refs に追加。複数回指定可
  --template <path>           template file。既定: docs/templates/operator-request-template.md
  --request-dir <path>        出力先 directory。既定: docs/exec-plans/operator-requests
  --opened-on <YYYY-MM-DD>    request 日付。既定: 今日
  --dry-run                   file を作らず、生成先だけ表示
  -h, --help                  この help を表示

Examples:
  add_operator_request.sh \
    --summary "次の chunk で article-source-map も見直したい" \
    --requested-role task-planner

  add_operator_request.sh \
    --summary "validation 章の構成を先に相談したい" \
    --requested-role plan-manager \
    --detail "中チャプター再編に影響するため" \
    --related-ref docs/exec-plans/plan-spec.md
EOF
}

die() {
  echo "$1" >&2
  exit 1
}

normalize_role() {
  case "${1:-}" in
    plan-manager|plan_manager)
      printf '%s\n' "plan_manager"
      ;;
    task-planner|task_planner)
      printf '%s\n' "task_planner"
      ;;
    task-worker|task_worker)
      printf '%s\n' "task_worker"
      ;;
    plan-owner|plan_owner)
      printf '%s\n' "plan_owner"
      ;;
    reviewer)
      printf '%s\n' "reviewer"
      ;;
    conductor)
      printf '%s\n' "conductor"
      ;;
    human-operator|human_operator)
      printf '%s\n' "human_operator"
      ;;
    *)
      return 1
      ;;
  esac
}

render_list_block() {
  local text="$1"

  if [[ -z "$text" ]]; then
    return 1
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -n "$line" ]]; then
      printf -- '- %s\n' "$line"
    else
      printf -- '-\n'
    fi
  done <<< "$text"
}

next_request_id() {
  local opened_on="$1"
  local request_dir="$2"
  local max_seq=0
  local path

  shopt -s nullglob
  for path in "$request_dir"/REQ-"$opened_on"-*.md; do
    local base seq
    base="$(basename "$path")"
    seq="${base#REQ-$opened_on-}"
    seq="${seq%.md}"
    if [[ "$seq" =~ ^[0-9]{3}$ ]] && ((10#$seq > max_seq)); then
      max_seq=$((10#$seq))
    fi
  done
  shopt -u nullglob

  printf 'REQ-%s-%03d\n' "$opened_on" "$((max_seq + 1))"
}

SUMMARY=""
REQUESTED_ROLE="task_planner"
DETAIL=""
EXPECTED_HANDLING=""
NOTES=""
INTERRUPT_MODE="after_current_ticket"
REQUESTED_BY="human_operator"
TARGET_SCOPE="-"
TEMPLATE_PATH="$DEFAULT_TEMPLATE"
REQUEST_DIR="$DEFAULT_REQUEST_DIR"
OPENED_ON="$(date +%F)"
DRY_RUN=0
RELATED_REFS=("docs/exec-plans/plan-spec.md")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --summary)
      SUMMARY="${2:?missing value for --summary}"
      shift 2
      ;;
    --requested-role)
      REQUESTED_ROLE="$(normalize_role "${2:?missing value for --requested-role}")" \
        || die "Unsupported requested role: ${2}"
      shift 2
      ;;
    --detail)
      DETAIL="${2:?missing value for --detail}"
      shift 2
      ;;
    --expected-handling)
      EXPECTED_HANDLING="${2:?missing value for --expected-handling}"
      shift 2
      ;;
    --notes)
      NOTES="${2:?missing value for --notes}"
      shift 2
      ;;
    --interrupt-mode)
      INTERRUPT_MODE="${2:?missing value for --interrupt-mode}"
      shift 2
      ;;
    --requested-by)
      REQUESTED_BY="${2:?missing value for --requested-by}"
      shift 2
      ;;
    --target-scope)
      TARGET_SCOPE="${2:?missing value for --target-scope}"
      shift 2
      ;;
    --related-ref)
      if [[ "${#RELATED_REFS[@]}" -eq 1 && "${RELATED_REFS[0]}" == "docs/exec-plans/plan-spec.md" ]]; then
        RELATED_REFS=()
      fi
      RELATED_REFS+=("${2:?missing value for --related-ref}")
      shift 2
      ;;
    --template)
      TEMPLATE_PATH="${2:?missing value for --template}"
      shift 2
      ;;
    --request-dir)
      REQUEST_DIR="${2:?missing value for --request-dir}"
      shift 2
      ;;
    --opened-on)
      OPENED_ON="${2:?missing value for --opened-on}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "Unknown option: $1"
      ;;
  esac
done

[[ -n "$SUMMARY" ]] || die "summary is required."
[[ -f "$TEMPLATE_PATH" ]] || die "template not found: $TEMPLATE_PATH"
[[ "$OPENED_ON" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || die "opened_on must be YYYY-MM-DD: $OPENED_ON"
[[ "$INTERRUPT_MODE" == "after_current_ticket" ]] || die "interrupt_mode は after_current_ticket のみ対応です: $INTERRUPT_MODE"

mkdir -p "$REQUEST_DIR"

REQUEST_ID="$(next_request_id "$OPENED_ON" "$REQUEST_DIR")"
OUTPUT_PATH="$REQUEST_DIR/$REQUEST_ID.md"
[[ ! -e "$OUTPUT_PATH" ]] || die "request file already exists: $OUTPUT_PATH"

if [[ -n "$DETAIL" ]]; then
  DETAIL_LINES="$(render_list_block "$DETAIL")"
else
  DETAIL_LINES=$'- 背景:\n- 何を変えたいか:\n- どの phase / block / chunk / ticket に影響するか:'
fi

if [[ -n "$EXPECTED_HANDLING" ]]; then
  EXPECTED_HANDLING_LINES="$(render_list_block "$EXPECTED_HANDLING")"
else
  EXPECTED_HANDLING_LINES=$'- `task-planner` に戻して chunk / ticket の追加で閉じられるか判断してほしい\n- 必要なら `plan-manager` へ上げてほしい\n- `conductor` が pending request として検知できればよい'
fi

if [[ -n "$NOTES" ]]; then
  NOTES_LINES="$(render_list_block "$NOTES")"
else
  NOTES_LINES=$'- current ticket の完了後に処理してよい\n- 急ぎなら、その理由を書く'
fi

RELATED_REFS_LINES=""
for ref in "${RELATED_REFS[@]}"; do
  RELATED_REFS_LINES+="  - ${ref}"$'\n'
done
RELATED_REFS_LINES="${RELATED_REFS_LINES%$'\n'}"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "status=dry-run"
  echo "request_id=$REQUEST_ID"
  echo "path=$OUTPUT_PATH"
  exit 0
fi

{
  while IFS= read -r line || [[ -n "$line" ]]; do
    case "$line" in
      "{{RELATED_REFS}}")
        printf '%s\n' "$RELATED_REFS_LINES"
        continue
        ;;
      "{{DETAIL_LINES}}")
        printf '%s\n' "$DETAIL_LINES"
        continue
        ;;
      "{{EXPECTED_HANDLING_LINES}}")
        printf '%s\n' "$EXPECTED_HANDLING_LINES"
        continue
        ;;
      "{{NOTES_LINES}}")
        printf '%s\n' "$NOTES_LINES"
        continue
        ;;
    esac

    line="${line//\{\{REQUEST_ID\}\}/$REQUEST_ID}"
    line="${line//\{\{INTERRUPT_MODE\}\}/$INTERRUPT_MODE}"
    line="${line//\{\{REQUESTED_ROLE\}\}/$REQUESTED_ROLE}"
    line="${line//\{\{OPENED_ON\}\}/$OPENED_ON}"
    line="${line//\{\{REQUESTED_BY\}\}/$REQUESTED_BY}"
    line="${line//\{\{TARGET_SCOPE\}\}/$TARGET_SCOPE}"
    line="${line//\{\{SUMMARY\}\}/$SUMMARY}"
    printf '%s\n' "$line"
  done < "$TEMPLATE_PATH"
} > "$OUTPUT_PATH"

echo "status=created"
echo "request_id=$REQUEST_ID"
echo "requested_role=$REQUESTED_ROLE"
echo "path=$OUTPUT_PATH"
