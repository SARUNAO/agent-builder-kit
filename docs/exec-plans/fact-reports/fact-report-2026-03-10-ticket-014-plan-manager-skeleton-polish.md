# Fact Report: `plan-manager でプロジェクトの骨子を組む` 章の推敲と根拠同期を行う

- ticket_id: TICKET-2026-03-10-014
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/plan-manager-skeleton.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-014-plan-manager-skeleton-polish.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-014-plan-manager-skeleton-polish.md`
- `sed -n '1,260p' src/plan-manager-skeleton.md`
- `sed -n '1,260p' docs/exec-plans/active/article-source-map.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-013-plan-manager-skeleton-draft.md`
- `mdbook build`

## 結果
- `plan-manager-skeleton.md` の表記ゆれとコードブロック表現を整えた
- `article-source-map.md` に fact-report と `.canvas` 補助アセットを追加し、章意図と根拠を同期した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - 本文の勢いは残しつつ、canonical 名や code block 表記だけを整える方向で推敲した
- gotcha:
  - `.canvas` 画像そのものを本文にどう差し込むかはまだ固定していない
- command:
  - `mdbook build` で推敲後も book が生成できることを確認した
- before / after:
  - before: source map 側に TICKET-013 の fact-report と prompt 抜粋反映がまだなかった
  - after: 本文と source map の根拠導線が一段そろった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `.canvas` 画像を本文へ埋め込むか、別の補助素材として扱うかは次段で再判断が必要

## scope breach
- なし

## 補足
- `TICKET-014` は `done` 昇格に必要な材料をそろえた。status 昇格自体は `task-planner` に渡す
