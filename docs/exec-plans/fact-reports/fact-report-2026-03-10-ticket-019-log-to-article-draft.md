# Fact Report: `開発ログからチュートリアル本文を組み立てる` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-019
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/process-to-article.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-010-log-to-article.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-019-log-to-article-draft.md`

## 実行したコマンド
- `sed -n '1,240p' docs/exec-plans/chunks/chunk-2026-03-10-010-log-to-article.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-019-log-to-article-draft.md`
- `sed -n '1,260p' docs/exec-plans/active/index.md`
- `sed -n '1,260p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`

## 結果
- `src/process-to-article.md` を新規作成し、planning docs、fact-report、active logs をどう本文へ変換するかを説明する草稿を追加した
- `src/SUMMARY.md` に `開発ログからチュートリアル本文を組み立てる` 章を追加した
- `decision-log`, `gotcha-log`, `command-log`, `before-after`, `article-source-map` の役割分担を章内へ取り込んだ
- 着手実態に合わせて `CHUNK-010` と `TICKET-019` を `in_progress` に更新した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - この章は「記事を書くコツ」ではなく、「開発中の記録をどう教材へ変換するか」に寄せた
- gotcha:
  - 開発ログを時系列のまま本文にすると読みにくいため、source map を間に置く説明が必要だった
- command:
  - `mdbook build` で新章追加後も book が生成できることを確認した
- before / after:
  - before: この章ファイル自体が存在しなかった
  - after: 記録から本文へ変換する流れを説明する草稿が追加された

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `article-source-map.md` との章同期は、後続の `TICKET-020` で行う

## 補足
- 次の `TICKET-020` では、本文の推敲と source map の章同期を行う
