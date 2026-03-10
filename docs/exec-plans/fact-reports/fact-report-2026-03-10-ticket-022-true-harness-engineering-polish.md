# Fact Report: `真のハーネスエンジニアリングへ至るには？` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-022
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/true-harness-engineering.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-011-true-harness-engineering.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-022-true-harness-engineering-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-022-true-harness-engineering-polish.md`
- `sed -n '1,320p' src/true-harness-engineering.md`
- `sed -n '1,320p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`
- `python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py --plan-spec docs/exec-plans/plan-spec.md --block-dir docs/exec-plans/blocks --chunk-dir docs/exec-plans/chunks --ticket-dir docs/exec-plans/tickets --reference-dir docs/references --vault-root . --canvas docs/exec-plans/canvas/development-flow.canvas`

## 結果
- `src/true-harness-engineering.md` の文面を推敲し、現状課題と拡張方針の流れを整理した
- `article-source-map.md` に `真のハーネスエンジニアリングへ至るには？` 章を追加し、章意図と根拠を同期した
- CI/CD、lint、レイヤードアーキテクチャ支援が kit 標準外である理由を、汎用性優先の設計判断としてそろえた
- 着手実態に合わせて `TICKET-022` を `in_progress` に更新した
- `mdbook build` は成功した
- `.canvas` の再同期は成功した

## 記録素材メモ
- decision:
  - 将来案の章は理想論に寄せすぎず、現在の kit の構造から拡張できる候補へ絞った
  - CI/CD、lint、アーキテクチャ支援は「不足」ではなく「標準範囲外」という整理で統一した
- gotcha:
  - 将来案の章は source map に追加し忘れると、後続の本文管理で抜けが出やすい
- command:
  - `mdbook build` で新章の推敲後も book が生成できることを確認した
- before / after:
  - before: 本文は草稿だけあり、source map にこの章が未登録だった
  - after: 本文と source map が同じ章意図でそろった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- 並列化や CI/CD add-on の具体仕様は、まだ本文では概念整理の段階に留まっている

## 補足
- 次の裁定では、`TICKET-022` を `done` に上げれば `CHUNK-011` の close 判断に入れる
