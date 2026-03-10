# Fact Report: 記録から記事素材マップを作る

- ticket_id: TICKET-2026-03-10-008
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `docs/exec-plans/active/index.md`
- `docs/exec-plans/active/article-source-map.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-008-article-source-map.md`

## 実行したコマンド
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-008-article-source-map.md`
- `sed -n '1,220p' docs/exec-plans/active/decision-log.md`
- `sed -n '1,220p' docs/exec-plans/active/gotcha-log.md`
- `sed -n '1,220p' docs/exec-plans/active/command-log.md`
- `sed -n '1,220p' docs/exec-plans/active/before-after.md`
- `find asset -maxdepth 3 -type f | sort`

## 結果
- 初期 4 章に対して、どの一次記録を根拠に使うかを `article-source-map.md` に整理した
- 各章ごとに「主な根拠」「使えそうな事実」「足りない記録」を分けて残した
- root `asset/` の補助スナップショットを、ファイル名ベースの補助素材として対応する章へ追記した

## 記録素材メモ
- decision:
  - 素材マップは `src/` 本文ではなく `docs/exec-plans/active/` に置き、章本文と一次記録の間の索引として扱うことにした
- gotcha:
  - 補助スナップショットは画像内容を断定せず、ファイル名ベースの補助根拠として扱う必要がある
  - role フロー章には reviewer が code ticket に入る実例がまだ不足している
- command:
  - 今回は既存記録、`src/` スタブ、`asset/` のファイル名を読むコマンドだけで章との対応を整理した
- before / after:
  - before: 根拠は 4 系統のログへ散在し、補助スナップショットも素材マップに結びついていなかった
  - after: 4 章それぞれがどの記録と補助アセットを読むべきかを 1 ファイルで辿れるようになった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- 画面キャプチャや可視化図など、本文の補助になる素材はまだ不足している
- `agent-builder-kit` 自体の実例が入ると、章構成や根拠マップは再調整が必要になる可能性がある
- 画像内容の詳細はこの turn では検証しておらず、ファイル名ベースで補助用途に留めている

## scope breach
- なし

## 補足
- 次 ticket に渡すべき事実: BLK-003 は `article-source-map.md` を起点に、各章で使う根拠と補助アセット、不足分を判断できる
