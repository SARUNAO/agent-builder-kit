# Fact Report: TICKET-2026-03-10-027 pages skeleton

## 実施したこと
- `book.toml` に GitHub Pages 公開向けの最小設定を追加した
- `.github/workflows/mdbook-pages.yml` を追加し、GitHub Actions で mdBook を build / upload / deploy する骨格を入れた
- `docs/exec-plans/tickets/ticket-2026-03-10-027-pages-skeleton.md` を `in_progress` に上げ、実施結果と検証結果を追記した

## 確認できた事実
- `mdBook` には `[output.html]` で `site-url` や `git-repository-url` を設定できる
- GitHub Pages の custom workflow は `configure-pages`, `upload-pages-artifact`, `deploy-pages` を使う構成にできる
- GitHub-hosted runner には Rust toolchain が含まれる前提で `cargo install mdbook` を実行できる
- workflow と deploy 設定の変更があるため、reviewer handoff が必要

## 検証
- `mdbook build`
- workflow YAML の目視確認

## 記録素材メモ
- decision:
  - 初回 publish は `mdbook build` を最小ゲートにした workflow 骨格に留める
  - 公開 URL 未確定部分は placeholder と TODO コメントで明示する
- gotcha:
  - GitHub Pages の project site URL は repo 名で変わるため、`site-url` は確定値をまだ入れられない
  - Actions artifact / Pages action は版差分があるため、後続 ticket で前提整理を残す
- command:
  - `mdbook build` は `book.toml` へ `[output.html]` を追加しても成功した
- before-after:
  - before: `book.toml` は book metadata だけで、workflow もなかった
  - after: 公開向けの config と Pages deploy workflow の骨格がそろった
