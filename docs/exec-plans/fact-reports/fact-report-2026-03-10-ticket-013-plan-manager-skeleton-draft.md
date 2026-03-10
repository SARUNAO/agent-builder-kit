# Fact Report: `plan-manager でプロジェクトの骨子を組む` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-013
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/plan-manager-skeleton.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-013-plan-manager-skeleton-draft.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-013-plan-manager-skeleton-draft.md`
- `sed -n '1,240p' src/plan-manager-skeleton.md`
- `sed -n '1,220p' src/SUMMARY.md`
- `sed -n '1,220p' docs/exec-plans/active/article-source-map.md`
- `mdbook build`

## 結果
- `src/SUMMARY.md` の章ラベルを `plan-manager でプロジェクトの骨子を組む` に変更した
- `src/plan-manager-skeleton.md` を、`plan-manager` の役割と使い方を説明する草稿へ差し替えた
- `plan-manager` が何を読み、何を更新し、なぜ最初に骨子を作るのかを章内で説明した
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - 旧 `環境確認` 章は、現状の章構成と重心がずれていたため、`plan-manager` の planning 行為を扱う章へ差し替えた
- gotcha:
  - chapter file path も内容に合わせて `plan-manager-skeleton.md` へ変更した
- command:
  - `mdbook build` で章ラベル変更と本文差し替え後も book が生成できることを確認した
- before / after:
  - before: `mdbook` や `cargo` の確認へ寄った短文だった
  - after: `plan-manager` の役割、生成物、使い方を説明する草稿になった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `plan-manager` に実際にどう依頼したかのプロンプト例は、後続推敲で補う余地がある

## scope breach
- あり
- `CHUNK-005` と `CHUNK-006` を `done` に上げ、`CHUNK-007` と `TICKET-013` を実行開始に合わせて `in_progress` へ更新した

## 補足
- 次の `TICKET-014` では、`article-source-map.md` と本文の同期を整えつつ、実例や言い回しを推敲していく
