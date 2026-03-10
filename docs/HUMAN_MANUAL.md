# Human Manual

## この docs の目的
- 人間がどこで判断し、何を AI に任せ、何を承認するかを明確にする

## 人間が判断すること
- 優先順位
- 要求の採否
- protected path を動かしてよいか
- 旧 docs を正本から外してよいか

## AI に任せること
- inventory の初回ドラフト
- gap の洗い出し
- adoption plan の叩き台
- block / chunk / ticket の更新

## mdBook 未導入時の扱い
- `BLK-002` 着手時に `mdbook --version` が通らなければ、まず導入前提の整理を優先する
- この project では、初回は `mdbook init`, `mdbook build`, `mdbook serve --open` を理解できれば十分とする
- 導入できなかった場合でも、その事実とエラー内容を `fact-report` へ残して次 ticket に渡す

## 一次記録の残し方
- `BLK-007` 以降は、各 ticket の `fact-report` に `decision / gotcha / command / before-after` へ再利用できる短いメモを残す
- そのメモは `docs/exec-plans/active/` 配下の記録 docs に後から移せる粒度であれば十分で、毎回 4 種類すべて必須ではない
- 人間は「長いログ全文」よりも、「何を決めたか」「どこで詰まったか」「何を打って何が起きたか」を優先して確認する
- 公開時にそのまま見せたくない内部判断は、一次記録では事実として残し、本文では要約する

## GitHub 公開時に人間が判断すること
- 初回 publish 後に、GitHub Pages の実公開 URL を README と本文へ反映する
- `agent-builder-kit/` と mdBook が同一 repo で読者に分かるかを確認する
- link check や追加 lint は、初回 publish 完了後の改善項目として別判断する

## migration 時の確認ポイント
- 現行 AI が `MIGRATION_START_HERE.md` を起点に作業しているか
- `docs/migration/project-inventory.md` が埋まっているか
- `docs/migration/gap-report.md` に open question が残っているか
- `docs/migration/adoption-plan.md` に段階導入 plan があるか

## protected path
- まだなし
