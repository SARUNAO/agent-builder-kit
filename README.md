# mdBook Workshop

`agent-builder-kit` を題材にした mdBook チュートリアルと、配布用 kit を同じ repository にまとめた公開用 repo です。

## 含まれるもの
- `agent-builder-kit/`
  - `AGENTS.md` や構造化された `docs/` を初期テンプレートとして展開するための kit
- `src/` と `book.toml`
  - mdBook 本文と設定

## 公開先
- GitHub Pages: `https://OWNER.github.io/REPO_NAME/`
- GitHub repository: `https://github.com/OWNER/REPO_NAME`

現在は placeholder 表記です。公開後に実 URL へ差し替えてください。

## ローカルで見る
1. `mdbook --version`
2. `mdbook build`
3. `mdbook serve --open`

出力先は `book/` です。`book/` は生成物なので repository には含めません。
