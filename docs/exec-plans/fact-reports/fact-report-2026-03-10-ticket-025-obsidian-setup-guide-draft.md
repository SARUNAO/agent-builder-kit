# Fact Report: TICKET-2026-03-10-025 obsidian setup guide draft

## 実施したこと
- `src/overview.md` に Obsidian の導入と Vault の開き方を追加した
- `.obsidian` と `.canvas` の関係を、`agent-builder-kit` 導入の文脈で分かるように補った
- `docs/exec-plans/tickets/ticket-2026-03-10-025-obsidian-setup-guide-draft.md` を `in_progress` に上げ、実施結果と検証結果を追記した

## 確認できた事実
- Obsidian は project を Vault として開くことで `.obsidian/` が生成される
- `.canvas` を使った開発フローの可視化は Obsidian 連携を前提にしているため、導入段階で触れておく価値がある
- 今回の更新は docs-only なので reviewer は skip でよい

## 検証
- `mdbook build`
- `src/overview.md` の目視確認

## 記録素材メモ
- decision:
  - Obsidian は独立した大きな節にせず、`新規プロジェクトを開始` の冒頭で最小手順だけ案内する
- gotcha:
  - Obsidian の詳細な使い方まで入れると chapter の重心がずれるため、Vault を開くところで止めるのがよい
- before-after:
  - before: `.obsidian/` の役割だけが書かれていた
  - after: Obsidian をいつ入れ、どこまで準備すればよいかが章単体で分かるようになった
