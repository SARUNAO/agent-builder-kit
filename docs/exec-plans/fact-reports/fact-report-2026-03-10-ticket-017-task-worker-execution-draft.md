# Fact Report: `task-worker で ticket を実行し、fact-report を返す` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-017
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/first-change.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-009-task-worker-execution.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-017-task-worker-execution-draft.md`

## 実行したコマンド
- `sed -n '1,240p' docs/exec-plans/chunks/chunk-2026-03-10-009-task-worker-execution.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-017-task-worker-execution-draft.md`
- `sed -n '1,260p' src/first-change.md`
- `sed -n '1,220p' src/SUMMARY.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-002-mdbook-init.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-004-local-verification.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-002-mdbook-init.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-004-local-verification.md`
- `mdbook build`

## 結果
- `src/first-change.md` を、`task-worker` の役割、ticket 実行、`fact-report` 返却、reviewer handoff を説明する草稿へ差し替えた
- `src/SUMMARY.md` の章ラベルを `task-worker で ticket を実行し、fact-report を返す` に更新した
- `TICKET-002` の reviewer handoff と、`TICKET-004` の docs-only skip を実例として本文へ取り込んだ
- 着手実態に合わせて `CHUNK-009` と `TICKET-017` を `in_progress` に更新した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - 章タイトルは抽象的な `最初の変更` ではなく、role と返り値が分かる `task-worker で ticket を実行し、fact-report を返す` に寄せた
  - reviewer は独立章にせず、この章の小見出しとして扱った
- gotcha:
  - `task-worker` の価値は実装そのものだけでなく、`fact-report` による事実返却まで含めて説明しないと伝わりにくい
- command:
  - `mdbook build` で章ラベル変更と本文差し替え後も book が生成できることを確認した
- before / after:
  - before: 小さな変更と記録の結びつきを示すだけの短いプレースホルダだった
  - after: `task-worker` の役割、入力、出力、reviewer handoff を説明する草稿になった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- この章にはまだ図版がなく、後続推敲で `fact-report` 画面や diff 例を入れる余地がある
- chapter file path `src/first-change.md` を章タイトルに合わせて変更するかは、後続 chunk 全体の命名とあわせて再判断してよい

## scope breach
- あり
- 利用者の指示に合わせて、`task-worker` 実行前に `CHUNK-009` を `pending -> in_progress` へ同期した

## 補足
- 次の `TICKET-018` では、本文の推敲と `article-source-map.md` の章同期を整える
