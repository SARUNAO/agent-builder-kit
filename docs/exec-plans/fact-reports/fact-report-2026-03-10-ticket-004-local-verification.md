# Fact Report: build / serve の確認手順を残す

- ticket_id: TICKET-2026-03-10-004
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `README.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-004-local-verification.md`

## 実行したコマンド
- `mdbook build`
- `timeout 5s mdbook serve --open --hostname 127.0.0.1 --port 3001`

## 結果
- `mdbook build` は成功し、`book/` に HTML を生成できた
- sandbox 内の `mdbook serve --open` は localhost bind 制約で `Operation not permitted (os error 1)` になった
- 制限外で同じ `mdbook serve --open` を実行すると、`http://127.0.0.1:3001` で watcher 起動まで確認できた
- README に build / serve の最小手順と、sandbox 制約時の見方を追加した

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新とコマンド確認のみで、コードパスや設定値の変更がないため

## 未解決事項
- `serve --open` で実際に開かれたブラウザ画面そのものは記録していない
- 将来 GitHub Pages を追加したら公開 URL 前提の確認手順を別 ticket で足す必要がある

## scope breach
- なし

## 補足
- command 候補: `mdbook build`, `mdbook serve --open`
- gotcha 候補: sandbox や headless 環境では localhost bind やブラウザ起動が失敗することがある
- before: ローカル検証の結果が repo に残っていなかった
- after: README と fact-report に build / serve の事実が残った
