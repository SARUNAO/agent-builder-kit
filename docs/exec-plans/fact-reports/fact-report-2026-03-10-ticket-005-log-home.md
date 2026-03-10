# Fact Report: 一次記録 docs の置き場と index を作る

- ticket_id: TICKET-2026-03-10-005
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `docs/exec-plans/active/index.md`
- `docs/exec-plans/active/decision-log.md`
- `docs/exec-plans/active/gotcha-log.md`
- `docs/exec-plans/active/command-log.md`
- `docs/exec-plans/active/before-after.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-005-log-home.md`

## 実行したコマンド
- `find docs/exec-plans/active -maxdepth 2 -type f | sort`
- `sed -n '1,220p' docs/exec-plans/active/index.md`

## 結果
- `docs/exec-plans/active/` 配下に一次記録のホームを作成した
- active index から decision / gotcha / command / before-after の 4 docs へ辿れるようにした
- 各 docs に役割と最小 template を入れ、本文ではなく一次記録の置き場であることを明記した

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- 実例の初回投入は次 chunk 後半の ticket で行う
- `fact-report` template 自体の拡張は TICKET-2026-03-10-006 で扱う

## scope breach
- なし

## 補足
- 運用時の注意: raw ログの全文貼り付けを避け、再利用しやすい粒度に留める
- article source 候補: どの種類の記録をどこへ残すか、そのままチュートリアルの説明材料に使える
