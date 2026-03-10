# Fact Report: `agent-builder-kit の導入` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-012
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/overview.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-012-agent-builder-kit-intro-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-012-agent-builder-kit-intro-polish.md`
- `sed -n '1,260p' src/overview.md`
- `sed -n '1,260p' docs/exec-plans/active/article-source-map.md`
- `sed -n '1,260p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-011-agent-builder-kit-intro-draft.md`
- `mdbook build`

## 結果
- `overview.md` の文面を整え、コードブロックの info string と表記ゆれを修正した
- `article-source-map.md` の該当節を `agent-builder-kit の導入` に改め、現在の本文内容と合うよう更新した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - 章タイトルは現時点では `agent-builder-kit の導入` を維持し、本文の推敲に合わせて source map 側も同期した
- gotcha:
  - GitHub 公開 repo の URL はまだ未確定のため、source map 側でも未解決事項として残した
  - `docs-builder.toml` の具体例や profile 選択理由は、今回の ticket ではまだ掘り下げていない
- command:
  - `mdbook build` で本文推敲後も book が生成できることを確認した
- before / after:
  - before: source map の章名と章意図が旧 `概要` ベースのまま残っていた
  - after: 本文と source map の章名、章意図、使えそうな事実が同期した

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `agent-builder-kit` の GitHub 公開後に、本文先頭の導線を実 URL へ差し替える必要がある
- `docs-builder.toml` の具体的な設定例は、後続 ticket で補う余地がある

## scope breach
- なし

## 補足
- `TICKET-012` は `done` 昇格に必要な材料をそろえた。status 昇格自体は `task-planner` に渡す
