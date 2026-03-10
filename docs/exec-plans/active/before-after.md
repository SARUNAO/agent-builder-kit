# Before / After

この docs は、変更前後で何が増えたか、何が変わったかを読者向けに再利用しやすい粒度で残す一次記録の置き場。

## 書き方
- before と after を対応させて書く
- ファイル名や構成の変化が分かる粒度に留める
- diff 全文ではなく、説明に必要な変化だけを書く

## Entries
- 2026-03-10 / BLK-002: before は `book.toml` と `src/` が存在しなかった。after は `mdbook v0.5.2`, `book.toml`, `src/SUMMARY.md`, `src/overview.md` がそろった。note: 最小骨格は `mdbook init` で生成した。
- 2026-03-10 / TICKET-2026-03-10-003: before は `SUMMARY.md` が 1 章構成だった。after は「概要」「環境確認」「role フロー体験」「最初の変更」の 4 章構成になった。note: 各章本文は最小スタブに留めている。
- 2026-03-10 / TICKET-2026-03-10-004: before はローカル検証結果が repo に残っていなかった。after は `README.md` と fact-report に `mdbook build` / `serve` の結果と制約が残った。note: `book/` は build 出力先として扱う。

## Template
- 日付:
- ticket / block:
- before:
- after:
- note:
