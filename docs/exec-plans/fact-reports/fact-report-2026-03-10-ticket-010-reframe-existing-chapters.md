# Fact Report: 既存 4 章の導入文を `agent-builder-kit` 主軸へ寄せる

- ticket_id: TICKET-2026-03-10-010
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/overview.md`
- `src/plan-manager-skeleton.md`
- `src/role-flow.md`
- `src/first-change.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-010-reframe-existing-chapters.md`

## 実行したコマンド
- `sed -n '1,240p' docs/exec-plans/tickets/ticket-2026-03-10-010-reframe-existing-chapters.md`
- `sed -n '1,240p' src/overview.md`
- `sed -n '1,240p' src/SUMMARY.md`
- `sed -n '1,240p' src/plan-manager-skeleton.md`
- `sed -n '1,240p' src/role-flow.md`
- `sed -n '1,240p' src/first-change.md`

## 結果
- `overview.md` を、実質的に `agent-builder-kit` の導入として読める冒頭へ調整した
- `src/SUMMARY.md` の章ラベルも `agent-builder-kit の導入` に変更した
- `plan-manager-skeleton.md` を、作業前の足場確認として位置づけ直した
- `role-flow.md` に、タスクの細分化と境界分離を見る章であることを追加した
- `first-change.md` に、変更と記録の結びつきを見る章であることを追加した

## 記録素材メモ
- decision:
  - 「はじめに」の次は `agent-builder-kit` の導入として読める流れにするため、`overview.md` を導入編として再定義した
- gotcha:
  - 最初の実装では `SUMMARY.md` の章ラベルが `概要` のまま残り、本文の重心と見出し表示がずれた
- command:
  - 今回は章冒頭の調整が目的なので、既存章の読み取りコマンドで現状確認を行った
- before / after:
  - before: 各章が短く、mdBook 一般入門にも見えうる説明だった
  - after: 4 章の冒頭だけでも `agent-builder-kit` tutorial の流れとしてつながり、章ラベルも本文の重心と一致するようになった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `SUMMARY.md` の章ラベル自体を「agent-builder-kit の導入」へ寄せるかどうかは、別 ticket で判断したほうがよい

## scope breach
- あり
- `src/SUMMARY.md` を追加で更新し、章ラベルを本文の重心に合わせた

## 補足
- 次に人間が本文を推敲するときは、`overview.md` を「導入方法」寄りにするか「思想と構造の紹介」寄りにするかをさらに詰められる
