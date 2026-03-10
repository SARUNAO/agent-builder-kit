# Fact Report: 「はじめに」章を追加し、この mdBook の骨子を最初に説明する

- ticket_id: TICKET-2026-03-10-009
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/introduction.md`
- `src/overview.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-009-introduction-chapter.md`

## 実行したコマンド
- `sed -n '1,220p' docs/exec-plans/tickets/ticket-2026-03-10-009-introduction-chapter.md`
- `sed -n '1,220p' src/SUMMARY.md`
- `sed -n '1,220p' src/overview.md`
- `sed -n '1,240p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`

## 結果
- `SUMMARY.md` の先頭に「はじめに」を追加した
- `src/introduction.md` を新規作成し、この mdBook が `agent-builder-kit` tutorial を主軸にしていることを明記した
- `src/overview.md` を、本論の入口として機能する短い説明へ調整した
- 人間レビューに基づき、導入文の表現、`扱うこと / 扱わないこと`、参考記事リンクを更新した
- 「はじめに」章から章内目次にあたる案内段落を削除した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - title page custom ではなく、まず「はじめに」章で主題と読み方を示す方針を採用した
  - 文体は planning docs より少しやわらかくしつつ、主題と非主題は明示する構成にした
  - ハーネスエンジニアリングの背景記事は本文中で短く参照し、詳細説明は別章へ持ち越す方針にした
- gotcha:
  - `overview.md` と役割が重なりやすいため、導入章は全体方針、概要章は本論への橋渡しに分けた
  - `扱うこと` と `主役にしないこと` は対比が弱かったため、見出しを `扱わないこと` に変更した
  - 「はじめに」で読む順番まで説明すると章内目次に見えやすいため、案内は `SUMMARY.md` 側へ寄せた
- command:
  - `mdbook build` で新規章追加後の `SUMMARY.md` と本文構成が成立することを確認した
- before / after:
  - before: 先頭章がなく、読み始めた時点で mdBook と `agent-builder-kit` の主従が伝わりにくかった
  - after: 「はじめに」で主題、扱うこと、扱わないこと、参考記事が先に分かる構成になった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- 既存 4 章の導入文はまだ mdBook 寄りのままなので、次の `TICKET-2026-03-10-010` で主題配分をさらに揃える必要がある

## scope breach
- なし

## 補足
- 次 ticket では、`introduction.md` で置いた主題配分 3:7 を `overview.md`, `plan-manager-skeleton.md`, `role-flow.md`, `first-change.md` に反映する
- 背景参照として使った記事:
  - [Qiita 記事](https://qiita.com/nogataka/items/43c01957fa1e54d9a079)
  - [OpenAI 公式記事](https://openai.com/ja-JP/index/harness-engineering/)
