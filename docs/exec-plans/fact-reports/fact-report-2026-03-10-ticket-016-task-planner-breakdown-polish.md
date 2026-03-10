# Fact Report: `task-planner で仕事を chunk と ticket に分ける` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-016
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/role-flow.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-008-task-planner-breakdown.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-016-task-planner-breakdown-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-016-task-planner-breakdown-polish.md`
- `sed -n '1,320p' src/role-flow.md`
- `sed -n '1,260p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`
- `python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py --plan-spec docs/exec-plans/plan-spec.md --block-dir docs/exec-plans/blocks --chunk-dir docs/exec-plans/chunks --ticket-dir docs/exec-plans/tickets --reference-dir docs/references --vault-root . --canvas docs/exec-plans/canvas/development-flow.canvas`

## 結果
- `src/role-flow.md` の typo と表記ゆれを修正した
- chunk 更新前後の図版キャプションを読みやすく整えた
- `article-source-map.md` の旧章名 `role フロー体験` を、現行の `task-planner で仕事を chunk と ticket に分ける` へ同期した
- 現行本文に合わせて、source map に `TICKET-015` の fact-report と `planner_chunk2.png` を追加した
- 着手実態に合わせて `TICKET-016` を `in_progress` に更新した
- `mdbook build` は成功した
- `.canvas` の再同期は成功した

## 記録素材メモ
- decision:
  - 推敲 ticket では章本文の大枠を変えず、章名同期と source map の更新を優先した
- gotcha:
  - 本文は更新されていても、`article-source-map.md` 側が旧章名のままだと後続の章管理でズレが残る
- command:
  - `mdbook build` で推敲後も表示崩れなく book が生成できることを確認した
- before / after:
  - before: 本文はほぼ整っていたが、source map が旧章名と旧意図のままだった
  - after: 本文と source map が同じ章意図でそろい、現行の図版構成も反映された

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `src/role-flow.md` というファイル名を章タイトルに合わせて変更するかは、後続 chunk 全体の命名とあわせて再判断してよい

## 補足
- 次の裁定では、`TICKET-016` を `done` に上げれば `CHUNK-008` の close 判断に入れる
