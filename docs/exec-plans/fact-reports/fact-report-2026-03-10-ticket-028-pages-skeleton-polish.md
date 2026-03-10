# Fact Report: TICKET-2026-03-10-028 pages skeleton polish

## 実施したこと
- reviewer 指摘を受けて、workflow 側で `book.toml` の placeholder を repository 情報から置換する手順を追加した
- `book.toml` の comment を、未確定値ではなく CI で解決する marker だと分かる表現へ直した
- `docs/exec-plans/active/attention-queue.md` に、publish 後に実 URL を本文と README へ反映する項目を追加した
- `docs/exec-plans/tickets/ticket-2026-03-10-028-pages-skeleton-polish.md` を `in_progress` に上げ、実施結果と検証結果を追記した

## 確認できた事実
- `github.repository_owner` と `github.event.repository.name` から Pages 用の project site パスを組み立てられる
- placeholder を workflow で解決すれば、source の `book.toml` に未確定値を固定せずに済む
- 実公開 URL の読者向け反映は、publish 完了後の別作業として切り分けるのが自然
- workflow と deploy 設定の変更が続くため、reviewer handoff が必要

## 検証
- `mdbook build`
- workflow YAML と `attention-queue.md` の目視確認

## 記録素材メモ
- decision:
  - reviewer finding は `book.toml` を即実値へ差し替えるのではなく、workflow で解決する方式で潰す
  - 実 URL を README / 本文へ書き戻す作業は post-publish の別項目へ分離する
- gotcha:
  - project site は repo 名で path が変わるため、source に固定値を置くと移植性が下がる
- before-after:
  - before: placeholder のまま build / deploy される前提だった
  - after: CI が repo 情報から placeholder を解決し、publish 後の docs 反映だけが残課題になった
