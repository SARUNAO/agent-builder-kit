# Fact Report: `開発ログからチュートリアル本文を組み立てる` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-020
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/process-to-article.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-010-log-to-article.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-020-log-to-article-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-020-log-to-article-polish.md`
- `sed -n '1,320p' src/process-to-article.md`
- `sed -n '1,360p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`
- `python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py --plan-spec docs/exec-plans/plan-spec.md --block-dir docs/exec-plans/blocks --chunk-dir docs/exec-plans/chunks --ticket-dir docs/exec-plans/tickets --reference-dir docs/references --vault-root . --canvas docs/exec-plans/canvas/development-flow.canvas`

## 結果
- `src/process-to-article.md` の文面を少しやわらかく推敲した
- この章が AI エージェント側の提案で立てられ、人間が採用した章であることを本文へ追記した
- `article-source-map.md` に `開発ログからチュートリアル本文を組み立てる` 章を追加し、章意図と根拠を同期した
- `TICKET-020` を `in_progress` に更新した
- `mdbook build` は成功した
- `.canvas` の再同期は成功した

## 記録素材メモ
- decision:
  - この章はやや説明的になりやすいため、少し柔らかい文脈へ寄せた
  - AI 側の発案で差し込まれた章であることも、project の性質を表す事実として本文へ残した
- gotcha:
  - source map にこの章が未登録のままだと、本文と根拠導線の同期が崩れる
- command:
  - `mdbook build` で推敲後も book が生成できることを確認した
- before / after:
  - before: 草稿はあったが、source map との同期がなく、章の立ち位置も少し硬かった
  - after: 章のトーンが少し柔らかくなり、根拠導線も明示された

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- この章に対応する図版はまだない

## 補足
- 次の裁定では、`TICKET-020` を `done` に上げれば `CHUNK-010` の close 判断に入れる
