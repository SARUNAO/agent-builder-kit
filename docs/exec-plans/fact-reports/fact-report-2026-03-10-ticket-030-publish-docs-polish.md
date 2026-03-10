# Fact Report: TICKET-2026-03-10-030 publish docs polish

## 実施したこと
- `src/overview.md` の公開前 placeholder を、同一 repo 公開前提が分かる表現へ整えた
- `src/conclusion.md` に、公開後は tutorial site と `agent-builder-kit` を同一 repo で行き来できる旨を追記した
- `docs/exec-plans/active/article-source-map.md` に公開導線の根拠を追加した
- `docs/exec-plans/tickets/ticket-2026-03-10-030-publish-docs-polish.md` を `in_progress` に上げ、実施結果と検証結果を追記した

## 確認できた事実
- 本文側にも、同一 repo と project Pages の関係を軽く入れておくと読者導線が閉じやすい
- 既存の章意図を崩さずに公開導線を差し込むなら、導入章とおわりにへ短く入れるのが自然
- 今回の更新は docs-only なので reviewer は skip でよい

## 検証
- `src/overview.md`, `src/conclusion.md`, `docs/exec-plans/active/article-source-map.md` の目視確認

## 記録素材メモ
- decision:
  - 公開導線は本文全体へ広げず、`overview` と `conclusion` へ短く差し込む
- gotcha:
  - 実公開 URL はまだないため、本文では構造説明に留め、実リンク反映は post-publish に回す
- before-after:
  - before: 公開導線は README 側にだけ寄っていた
  - after: 本文側でも同一 repo の読み方が分かるようになった
