# Fact Report: `真のハーネスエンジニアリングへ至るには？` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-021
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/true-harness-engineering.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-021-true-harness-engineering-draft.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/chunks/chunk-2026-03-10-011-true-harness-engineering.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-021-true-harness-engineering-draft.md`
- `sed -n '1,220p' src/SUMMARY.md`
- `mdbook build`

## 結果
- `src/true-harness-engineering.md` を新規作成し、現状の到達点、限界、拡張候補を整理する草稿を追加した
- `src/SUMMARY.md` に `真のハーネスエンジニアリングへ至るには？` 章を追加した
- OpenAI の Harness Engineering 記事を参照し、評価、足場、運用設計を含む観点を本文へ反映した
- CI/CD やレイヤードアーキテクチャ支援を kit に標準同梱していない理由として、「project 依存が強く、汎用性を優先した」旨を本文に明記した
- Rust の Clippy を例に、リンターや static analysis も有効だが kit の標準範囲外であることを本文へ追記した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - この章は理想論ではなく、「今ある kit をどう拡張すると本格運用へ近づくか」に寄せた
  - CI/CD やレイヤードアーキテクチャ支援は、欠陥としてではなく、汎用性優先であえて外している設計判断として書いた
  - リンターも同様に、品質強化手段としては有効だが project 依存が強いため標準同梱しない整理にした
- gotcha:
  - 将来案の章は抽象論に流れやすいため、現在の docs 駆動フローと接続する表現が必要だった
- command:
  - `mdbook build` で新章追加後も book が生成できることを確認した
- before / after:
  - before: この章ファイル自体が存在しなかった
  - after: 将来拡張の方向性を整理する草稿が追加された

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `.canvas` の並列実行色分けや multi-agent ルールは、まだ構想レベルで実装詳細には落としていない
- OpenAI 記事をどの程度本文中で直接引用するかは、後続推敲で調整の余地がある

## 補足
- 次の `TICKET-022` では、本文の推敲と `article-source-map.md` の章同期を行う
