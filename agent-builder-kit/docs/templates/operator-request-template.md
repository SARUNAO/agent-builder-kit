---
request_id: {{REQUEST_ID}}
status: pending
interrupt_mode: {{INTERRUPT_MODE}}
requested_role: {{REQUESTED_ROLE}}
opened_on: {{OPENED_ON}}
requested_by: {{REQUESTED_BY}}
target_scope: {{TARGET_SCOPE}}
related_refs:
{{RELATED_REFS}}
kind: operator_request
---

# Operator Request

loop 実行中に、人間が「この ticket のあとで差し込みたい要望」を残すための template。

## summary
- {{SUMMARY}}

## detail
{{DETAIL_LINES}}

## expected_handling
{{EXPECTED_HANDLING_LINES}}

## notes
{{NOTES_LINES}}

## status guide
- `pending`: まだ未確認
- `acknowledged`: loop が検知し、次の role へ返す判断待ち
- `resolved`: 関連 docs へ反映済み
- `obsolete`: もう不要
