# Fact Report: `fact-report` と記録ルールを揃える

- ticket_id: TICKET-2026-03-10-006
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `docs/templates/fact-report-template.md`
- `README.md`
- `docs/HUMAN_MANUAL.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-006-fact-report-contract.md`

## 実行したコマンド
- `sed -n '1,260p' docs/templates/fact-report-template.md`
- `sed -n '1,260p' README.md`
- `sed -n '1,240p' docs/HUMAN_MANUAL.md`

## 結果
- `fact-report` template に `decision / gotcha / command / before-after` へ再利用しやすい欄を追加した
- `README.md` に BLK-007 以降の記録ルールを追記した
- `docs/HUMAN_MANUAL.md` に、人間が確認する一次記録の粒度を追記した

## 記録素材メモ
- decision:
  - 一次記録は毎回 4 種類すべて必須にはせず、ticket ごとに意味のある事実だけ返す方針にした
- gotcha:
  - 記録ルールを厳しくしすぎると worker の負荷が上がるため、template では「なし」を許容する形にした
- command:
  - 今回は説明整備が目的なので、確認用の `sed` 読み取りコマンドだけを使った
- before / after:
  - before: `fact-report` template は結果と reviewer 結果だけを中心にしていた
  - after: 記録 block が再利用しやすい `記録素材メモ` と書き方の目安が加わった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- 実例ログの retro 収集は次 chunk 後半で実施する
- 実運用で template が重すぎるかどうかは、数 ticket 運用してから再確認が必要

## scope breach
- なし

## 補足
- 次 ticket に渡すべき事実: 後続 worker は `fact-report` 内の `記録素材メモ` を起点に、必要な項目だけ短く残せばよい
