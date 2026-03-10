# Fact Report: `agent-builder-kit の導入` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-011
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/overview.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-011-agent-builder-kit-intro-draft.md`

## 実行したコマンド
- `sed -n '1,240p' docs/exec-plans/chunks/chunk-2026-03-10-006-agent-builder-kit-intro.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-011-agent-builder-kit-intro-draft.md`
- `sed -n '1,240p' src/overview.md`
- `sed -n '1,200p' AGENTS.md`
- `mdbook build`

## 結果
- `overview.md` を、新規プロジェクトで `agent-builder-kit` を初期化する導入に差し替えた
- 公開 repo への導線を置く前提で、公開前の注意書きを本文先頭に追加した
- 章の入口として、最初の節見出しを `新規プロジェクトを開始` に整理した
- ルート直下に並ぶ `.obsidian`, `agent-builder-kit`, `docs-builder.toml` をコードブロックで示した
- 各項目の役割は、目次に出ないフラットな箇条書きで説明し、次章の `plan-manager` 章へつながる終わり方にした
- `mdbook build` は成功した

## 記録素材メモ
- decision:
  - 既存の抽象的な導入文は今回の目的に合わないため、初期化手順の入口へ丸ごと差し替えた
  - 章タイトルは維持しつつ、本文は「導入方法」に寄せた
- gotcha:
  - ユーザーの最初のメッセージでは `agent-builder.toml` と書かれていたが、その後の詳細説明は `docs-builder.toml` にそろっていたため、本文では後者を採用した
  - 公開 repo はまだ存在しないため、URL は埋めずに「公開後に差し替える」注意書きで止めた
- command:
  - `mdbook build` で章差し替え後も book が生成できることを確認した
- before / after:
  - before: `agent-builder-kit` と mdBook の位置づけを抽象的に説明する短文だった
  - after: 新規プロジェクトを開いて最初に何を置くかが、コードブロック付きで分かる導入になった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `docs-builder.toml` の具体的な編集例や profile 選択の説明は、この ticket ではまだ書いていない
- `agent-builder-kit` の GitHub 公開後に、本文先頭の導線を実 URL へ差し替える必要がある

## scope breach
- あり
- `CHUNK-006` の status と chunk 内 ticket table を、実行開始の roll-up 整合として `in_progress` へ更新した

## 補足
- 次の `TICKET-012` では、本文推敲に合わせて章タイトルを `導入方法` 寄りへ寄せるかどうかも再判断できる
