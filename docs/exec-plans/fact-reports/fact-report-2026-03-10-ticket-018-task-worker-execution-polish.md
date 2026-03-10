# Fact Report: `task-worker で ticket を実行し、fact-report を返す` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-018
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/first-change.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-009-task-worker-execution.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-018-task-worker-execution-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-018-task-worker-execution-polish.md`
- `sed -n '1,320p' src/first-change.md`
- `sed -n '1,260p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`
- `python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py --plan-spec docs/exec-plans/plan-spec.md --block-dir docs/exec-plans/blocks --chunk-dir docs/exec-plans/chunks --ticket-dir docs/exec-plans/tickets --reference-dir docs/references --vault-root . --canvas docs/exec-plans/canvas/development-flow.canvas`

## 結果
- `src/first-change.md` の文面を推敲し、`task-worker` の責務、`fact-report` の価値、reviewer handoff の切り分けを読みやすく整えた
- ticket 完了後に `task-planner` と `plan-manager` へ結果を返し、status を昇華させる流れを本文へ追加した
- `article-source-map.md` の旧章名 `最初の変更` を、現行の `task-worker で ticket を実行し、fact-report を返す` へ同期した
- `TICKET-017` の草稿内容と現行本文に合わせて、source map の章意図と根拠を更新した
- 着手実態に合わせて `TICKET-018` を `in_progress` に更新した
- `mdbook build` は成功した
- `.canvas` の再同期は成功した

## 記録素材メモ
- decision:
  - 推敲 ticket では本文の流れを大きく変えず、source map との章名同期と返却物の説明強化を優先した
  - 上流への status 昇華は別章に分けず、この章の返却物説明の中へ含めた
- gotcha:
  - 本文を更新しても、source map が旧章名のままだと後続の本文管理でズレが残る
- command:
  - `mdbook build` で推敲後も表示崩れなく book が生成できることを確認した
- before / after:
  - before: 本文は読める状態だったが、source map が旧章名のままで章意図も弱かった
  - after: 本文と source map が同じ章タイトルと章意図でそろった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `fact-report` の見た目を直接見せる図版はまだない
- chapter file path `src/first-change.md` を章タイトルに合わせて変更するかは、後続 chunk 全体の命名とあわせて再判断してよい

## 補足
- 次の裁定では、`TICKET-018` を `done` に上げれば `CHUNK-009` の close 判断に入れる
