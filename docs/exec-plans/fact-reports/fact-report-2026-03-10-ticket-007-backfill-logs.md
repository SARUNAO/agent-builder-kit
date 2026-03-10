# Fact Report: BLK-002 の実例を decision / gotcha / command / before-after に落とす

- ticket_id: TICKET-2026-03-10-007
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `docs/exec-plans/active/decision-log.md`
- `docs/exec-plans/active/gotcha-log.md`
- `docs/exec-plans/active/command-log.md`
- `docs/exec-plans/active/before-after.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-007-backfill-logs.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-007-backfill-logs.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-001-mdbook-prereq.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-002-mdbook-init.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-003-summary-and-stubs.md`
- `sed -n '1,240p' docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-004-local-verification.md`

## 結果
- BLK-002 の事実を、`decision / gotcha / command / before-after` の 4 系統へ整理して追記した
- 章構成、導入判断、`mdbook init`、`mdbook build`、`mdbook serve --open` の制約を一次記録として再利用できる形にした
- 本文向けの解釈は避け、BLK-002 の fact-report に書かれていた事実だけを使った

## 記録素材メモ
- decision:
  - 初学者向け入口を README に寄せたこと、`mdbook init` 採用、日本語スタブ化、`mdbook build` を最低ゲートにしたことを回収した
- gotcha:
  - `mdbook` 未導入時の進め方、sandbox での localhost bind 制約、ブラウザ画面自体は未記録である点を回収した
- command:
  - `mdbook init`, `mdbook build`, `serve --open`, 章ファイル確認コマンドを回収した
- before / after:
  - 骨格未作成 -> 最小骨格作成、1 章 -> 4 章、検証未記録 -> README / fact-report へ反映、を回収した

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `cargo install mdbook` の所要時間や install 中ログは記録していない
- `serve --open` で実際に開いたブラウザ画面キャプチャは残っていない
- 今回は BLK-002 だけを対象にしたため、BLK-007 自身の運用実例はまだ回収していない

## scope breach
- なし

## 補足
- 次 ticket に渡すべき事実: active logs から章ごとの根拠を引ける状態になったので、次は記事素材マップへ整理できる
