# Command Log

この docs は、記事化や再現に必要なコマンドと、その結果の要約を残す一次記録の置き場。

## 書き方
- コマンド全文は必要な場合だけ残す
- 目的と結果を先に書き、ログ全文の貼り付けは避ける
- 失敗時は、次にどう扱うべきかも短く残す

## Entries
- 2026-03-10 / TICKET-2026-03-10-001: `mdbook --version` と `cargo install mdbook` を README に載せ、導入確認と未導入時の次手が分かるようにした。結果として、導入前でも BLK-002 に着手できる入口ができた。
- 2026-03-10 / TICKET-2026-03-10-002: `mdbook init --force --title "mdBook Workshop" .` を repo root で実行し、`book.toml` と `src/` の最小骨格を生成した。結果として、後続 ticket が章追加と検証へ進める状態になった。
- 2026-03-10 / TICKET-2026-03-10-003: `find src -maxdepth 2 -type f | sort` と `test -f ...` で章ファイルの存在を確認した。結果として、`SUMMARY.md` と 4 章スタブの対応が取れていることを確認できた。
- 2026-03-10 / TICKET-2026-03-10-004: `mdbook build` は成功し、`book/` に HTML を生成した。結果として、最低限のローカル build が通ることを確認できた。
- 2026-03-10 / TICKET-2026-03-10-004: `timeout 5s mdbook serve --open --hostname 127.0.0.1 --port 3001` は sandbox 内では `Operation not permitted (os error 1)` になったが、制限外では watcher 起動まで確認できた。

## Template
- 日付:
- ticket / block:
- command:
- purpose:
- result:
