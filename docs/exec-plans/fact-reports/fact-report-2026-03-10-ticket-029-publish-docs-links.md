# Fact Report: TICKET-2026-03-10-029 publish docs links

## 実施したこと
- `README.md` に GitHub Pages の公開導線 placeholder と repo 構造の説明を追加した
- `docs/HUMAN_MANUAL.md` に、GitHub 公開時に人間が確認 / 判断することを追加した
- `docs/exec-plans/tickets/ticket-2026-03-10-029-publish-docs-links.md` を `in_progress` に上げ、実施結果と検証結果を追記した

## 確認できた事実
- 読者向けには、公開 site と GitHub repository を README から直接追える形にしたほうが分かりやすい
- 同一 repo に `agent-builder-kit/` と mdBook があることは、README で明示したほうが誤解が少ない
- 今回の更新は docs-only なので reviewer は skip でよい

## 検証
- `README.md` と `docs/HUMAN_MANUAL.md` の目視確認

## 記録素材メモ
- decision:
  - 公開 URL は未確定なので README では placeholder を明示し、publish 後差し替え前提にする
- gotcha:
  - workflow で Pages 用 URL を解決していても、読者向け docs には実 URL を別で書き戻す必要がある
- before-after:
  - before: README と Human Manual に公開 site / repo 構造の説明がなかった
  - after: 公開後にどこを見ればよいかと、人間が何を判断するかが docs に残った
