# Obsidian Canvas Sync

この docs は、Obsidian `.canvas` を使って現在の開発フロー進捗を可視化し、docs の更新と同期させる add-on の設計。

## 目的
- `plan-spec`, `chunk-sheet`, `ticket` の階層を視覚化する
- 上流で plan が変わったときに、chunk と ticket のつながりも一緒に追えるようにする
- 人間が Obsidian 上で「今どこにいるか」を素早く確認できるようにする

## add-on の位置づけ
- 名前: `obsidian_canvas_pack`
- 既定 profile には含めない
- `expanded` で必要に応じて追加する
- repo には skill bundle と `.canvas` の正本ファイルを置く

## 生成対象
- `docs/OBSIDIAN_CANVAS_SYNC.md`
- `docs/exec-plans/canvas/development-flow.canvas`
- `tools/codex-skills/obsidian-canvas-sync/SKILL.md`

## source of truth
- `.canvas` 自体は正本ではない
- 正本は以下の docs
  - `plan-spec`
  - `chunk-sheet`
  - `ticket`
  - `docs/PRODUCT_SENSE.md`
  - `docs/DESIGN.md`
  - `docs/HUMAN_MANUAL.md`
  - `docs/exec-plans/active/attention-queue.md`
- optional summary / hub docs として `docs/references/*.md` を残してよい
- `.canvas` はこれらを読み、再同期で再構成する可視化レイヤー

## reference band の正本契約
- canvas 上段の reference band は `direct-source` を正契約とし、本体 docs を直接読む
- 本体 docs は次の 4 つとする
  - `Product Sense` -> `docs/PRODUCT_SENSE.md`
  - `Design` -> `docs/DESIGN.md`
  - `Attention Queue` -> `docs/exec-plans/active/attention-queue.md`
  - `Human Manual` -> `docs/HUMAN_MANUAL.md`
- 本体 docs には `reference_id`, `title`, `lane_order`, `owner_role`, `sync_mode: direct_source` の frontmatter を置く
- `docs/references/*.md` は残す場合も optional summary / hub として扱い、band の代替正本にはしない
- generic 配布 package 自体には project-specific な reference note を同梱しなくてよい
- bootstrap 後に summary note を残す場合は、本体 docs への従属関係を明示する
- `TICKET-2026-03-11-025` 完了前は、実装が旧 `docs/references/*.md` 入力のままでも、契約上は移行途中として扱う

## block の扱い
- block の正本は `plan-spec` の `High-level blocks` テーブルとする
- `docs/exec-plans/blocks/*.md` は block の詳細メモや Obsidian 表示改善のための補助ノートとする
- `.canvas` の managed node は block/chunk/ticket を問わず text node を使う
- `docs/exec-plans/blocks/*.md`, `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md` が存在する場合は、node の先頭タイトルを markdown link にして対象 note へ飛べるようにする
- つまり block の存在判定、順序、status は `plan-spec` を見る

## 可視化モデル

### 縦列 A
- source:
  - `plan-spec` の `High-level blocks`
- ノード:
  - 高レベル block

### 縦列 B
- source:
  - `chunk-sheet`
- ノード:
  - chunk
- 接続:
  - `parent_block` で A の block と結ぶ

### 縦列 C
- source:
  - `ticket`
  - または `chunk-sheet` の ticket 一覧
- ノード:
  - ticket
- 接続:
  - `parent_chunk` で B の chunk と結ぶ
- 配置:
  - 同じ chunk に属する ticket を横に並べる

### 上段中央 reference band
- source:
  - `docs/PRODUCT_SENSE.md`
  - `docs/DESIGN.md`
  - `docs/exec-plans/active/attention-queue.md`
  - `docs/HUMAN_MANUAL.md`
- ノード:
  - `PRODUCT_SENSE`
  - `DESIGN`
  - `attention-queue`
  - 人間向けマニュアル
- 接続:
  - edge は張らない
- 配置:
  - 進捗フローの上段中央へ固定配置する
  - B/C レーンの中央に寄せて横並びにする

## edge ルール
- block は `plan-spec` の並び順で次の block へ接続する
- 各 block は、その block に属する最初の chunk にだけ接続する
- 同じ block に属する chunk は、上から下へ順番に接続する
- ticket は従来どおり親 chunk から横展開する

## 同期に必要な識別子

### block
- `block_id`
- `title`
- `status`

### chunk
- `chunk_id`
- `parent_block`
- `status`

### ticket
- `ticket_id`
- `parent_chunk`
- `status`

この 3 つが欠けると安全な差分同期ができない。

## source docs への要求

### 共通
- 同期用メタは YAML frontmatter を優先する
- 互換性のため `- key: value` 形式の bullet metadata も fallback で許可する
- parser は frontmatter を見つけたら、そちらを正本として扱う

### plan-spec
- `High-level blocks` テーブルを持つ
- 各 block に `block_id` を付ける

### block note
- 任意
- `block_id` と `title` を frontmatter に持つ
- `.canvas` 上の block タイトルから詳細 note へ飛ばしたいときに使う

### chunk-sheet
- `parent_block` を持つ
- ticket 一覧の順序を保持する

### ticket
- `parent_chunk` を持つ
- status を持つ

### reference source doc
- `Product Sense`, `Design`, `Human Manual`, `Attention Queue` の本体 docs に適用する
- `reference_id` と `title` を frontmatter に持つ
- `lane_order` で上段中央 band の並びを制御する
- `owner_role` を frontmatter に持ち、誰が更新責務を持つかを明示する
- `sync_mode: direct_source` を frontmatter に持つ
- band ノードはこの docs 自体を直接開く

### optional summary / hub note
- 任意
- `reference_id` と `title` を frontmatter に持つ
- `source_doc` を frontmatter に持ち、本体 docs への従属関係を明示する
- `sync_mode` を frontmatter に持ち、`summary_mirror` または `runtime_summary` を宣言する
- `owner_role` を frontmatter に持ち、誰が更新責務を持つかを明示する
- `lane_order` は summary / hub 内での並びや互換用途に使ってよい
- 進捗 edge には参加しない
- band integrity の唯一条件にはしない

## 現在の path 契約
- `.canvas` の正本は `docs/exec-plans/canvas/development-flow.canvas`
- reference band の正契約は本体 docs の direct-source とする
- source docs は `docs/exec-plans/plan-spec.md`, `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md` を使う
- optional summary / hub docs を残す場合だけ `docs/references/*.md` を読む

## reference band の更新責務
- `docs/PRODUCT_SENSE.md`
  - owner: `plan-owner`
  - trigger: 価値仮説、対象ユーザー、成功条件が変わったとき
- `docs/DESIGN.md`
  - owner: `plan-owner`
  - trigger: 構成判断、責務境界、設計前提が変わったとき
- `docs/exec-plans/active/attention-queue.md`
  - owner: `task-planner`
  - trigger: attention の追加、解消、優先順位変更が起きたとき
- `docs/HUMAN_MANUAL.md`
  - owner: `plan-owner`
  - trigger: 人間判断ルール、禁止事項、介入ポイントが変わったとき
- `docs/references/*.md`
  - owner: 本体 docs と同じ role、または将来の `docs-sync`
  - trigger: summary / hub を残す判断をしたうえで、本体 docs を更新したとき

## sync 起点の現時点判断
- role skill 自体は本体 docs の更新責務を持つ
- role skill はまず本体 docs を更新する
- optional summary / hub docs を残す場合だけ、同ターンで追従要否を判断する
- `.canvas` 再同期は source docs 更新後に行う
- `TICKET-2026-03-11-025` 完了前は script 実装が `docs/references/*.md` を読んでいても、contract drift ではなく移行途中として扱う

## ノード配置ルール

### 列の固定
- A 列: `x = 0`
- B 列: `x = 620`
- C 列: `x = 1240`
- reference band: `y = -280`
- 予備列 D: `x = 3600`
  - 手動メモや補助ノード用

### 行の決め方
- A 列は `plan-spec` の block テーブル順
- B 列は `parent_block` ごとにグループし、その中で `chunk_id` 順
- C 列は `chunk-sheet` 内の ticket 順

## 縦揃えルール
- 1 chunk = 1 row を基本単位とする
- 同じ chunk に属する ticket 群は、その chunk と同じ row の `y` と `height` を共有する
- block は、その block に属する chunk row 全体を覆う 1 ノードとして描画する
- つまり、ある block に 3 chunk あるなら、その block ノードは 3 row 分の高さまで縦に伸びる
- block ノード自体は 1 つのままでよい

### 例
- `BLK-A` に `CHUNK-A1`, `CHUNK-A2`, `CHUNK-A3` がある
- `CHUNK-A1` の ticket は横に並ぶが、すべて `CHUNK-A1` と同じ row 高さを使う
- `BLK-A` は `CHUNK-A1` から `CHUNK-A3` までの全 row を覆う高さになる

## status 表現
- `pending`
  - light slate blue `#94A3B8`
- `in_progress`
  - green `#10B981`
- `done`
  - white `#FFFFFF`
- `blocked`
  - red `#B91C1C`
- `obsolete`
  - faded

## 更新ルール

### 新 block が追加されたとき
- A 列に新ノードを追加する
- 既存の B/C ノードは stable id を維持したまま再配置する
- block 間 edge も table 順に再計算する
- したがって `plan-owner` は block 追加時に、`plan-spec` のどこへ差し込むかを必ず決める
- 後から依存関係や優先順が変わった場合は、`plan-spec` の table 順を見直してから再同期する

### block 順序の運用ルール
- `.canvas` の A 列順は `plan-spec` の `High-level blocks` テーブル順をそのまま使う
- `depends_on` だけでは block の縦順は変わらない
- 途中追加 block がある場合、`plan-owner` は
  - 追加直後の差し込み位置
  - 既存 block との前後関係が依然として妥当か
  を source docs 上で判断してから sync する

### chunk が追加されたとき
- `parent_block` を見て B 列へ追加する
- 既存 chunk の node id は保持する
- block 内の chunk edge は先頭から末尾まで引き直す

### ticket が追加されたとき
- 対応する chunk の行に C 列へ追加する

### 手戻りや仕様変更が起きたとき
- docs を先に更新する
- skill が docs を読み、`.canvas` を再同期する
- `.canvas` を手編集して source docs の代わりにしない

## 手編集との境界
- A/B/C の予約列内の node 位置は skill が管理する
- 上段中央の reference band も skill が管理する
- D 列以右のメモノードは保持する
- 予約列内に手動で追加された不明ノードは、削除せず D 列へ退避する

## skill の責務
- source docs を読む
- stable id に基づいて node/edge を更新する
- レイアウトを再計算する
- 予約列外の人手ノートは保持する

## 実装方式の結論
- skill 単体で JSON を手編集するのではなく、skill + bundled script の構成にする
- skill は次の役割を持つ
  - どの docs を読むか判断する
  - 必須識別子が欠けていないか確認する
  - script を実行する
  - 実行結果を検証し、必要なら再実行や差分確認を行う
- script は次の役割を持つ
  - markdown source docs を parse する
  - `.canvas` JSON を生成または更新する
  - node/edge の stable id と座標を決定的に計算する

## なぜ script を分けるか
- `.canvas` は JSON で、決定的更新が必要
- node の再配置や退避処理は毎回同じロジックで動いた方が安全
- skill の本文に JSON 更新ロジックを埋め込むと長くなり、保守しづらい
- 将来 builder から直接 script を叩く流れにも再利用できる

## 採用言語
- 第一候補は `Python`
- 理由:
  - 標準ライブラリで JSON とファイル操作が十分できる
  - text parsing を書きやすい
  - WSL / Linux / macOS で通しやすい
  - script skill の同梱先として扱いやすい

## 今回見送る案
- pure skill
  - 小さい更新には使えるが、決定的レイアウト更新には不向き
- Node.js
  - JSON 操作は強いが、repo に JS runtime 前提を増やしたくない段階では優先度が低い
- Rust
  - 実装は堅いが、skill 付属 script としては初速が重い

## skill ディレクトリ構成

```text
tools/codex-skills/obsidian-canvas-sync/
├── SKILL.md
└── scripts/
    └── sync_canvas.py
```

## script の責務分解

### `sync_canvas.py`
- 入力:
  - `--plan-spec`
  - `--chunk-dir` または `--chunk-sheet`
  - `--ticket-dir` または `--ticket`
  - `--reference-dir`
  - `--canvas`
  - `--manual-lane-x`
- 出力:
  - `.canvas` 更新
  - summary JSON または stdout summary

### 最小アルゴリズム
1. source docs を読む
2. `block_id`, `chunk_id`, `ticket_id` を収集する
3. lane A/B/C のノード配列を組む
4. existing `.canvas` を読んで managed / unmanaged を分離する
5. managed lanes を再生成する
6. unmanaged nodes を保持したまま書き戻す

## 実装段階の優先順位
1. 新規生成のみ
2. 既存 `.canvas` の managed lane 再構築
3. 手動ノート退避
4. status 色分けと edge 補正

## builder input への追加項目
- `workflow.packs` に `obsidian_canvas_pack`
- `[obsidian]` セクション
  - `vault_root`
  - `canvas_path`
  - `reference_dir`
  - `reserve_manual_lane`
  - `sync_on_chunk_close`

## 推奨配置
- `.canvas` は `.obsidian/` 配下ではなく、vault から見える通常フォルダへ置く
- 既定値は `docs/exec-plans/canvas/development-flow.canvas`
- legacy path は manifest override を使う場合だけ例外的に許容する
- 理由:
  - Obsidian のファイルペインから直接開ける
  - Git 管理しやすい
  - hidden directory に入れて「見えない」状態を避けられる

## Bitcoin dashboard 例
- A 列
  - `BLK-GUI`
  - `BLK-PRICE`
  - `BLK-NEWS`
- B 列
  - `CHUNK-PRICE-API`
  - `CHUNK-NEWS-API`
  - `CHUNK-DASHBOARD-UI`
- C 列
  - `TICKET-PRICE-POLLING`
  - `TICKET-NEWS-LIST`
  - `TICKET-BTC-CARD`

## 実装メモ
- `.canvas` は JSON なので、skill では決定的に更新できる
- parser は markdown の自由文ではなく、frontmatter と見出し配下の表を優先して読む
- 差分適用よりも「予約列だけ再構築」の方が安定する
