# Operational Schema

この docs は、builder が初期生成した後に、`プランオーナー`、`タスクプランナー`、`タスクワーカー + reviewer` が日々更新する運用上の正本 schema を定義する。

## 目的
- `.canvas` の手前にある source of truth を固定する
- role ごとの更新権限と更新順を明文化する
- block / chunk / ticket の整合制約を固定する

## source of truth
- 高レベル計画の正本:
  - `docs/exec-plans/plan-spec.md`
- block の補助 note:
  - `docs/exec-plans/blocks/*.md`
- chunk の正本:
  - `docs/exec-plans/chunks/*.md`
- ticket の正本:
  - `docs/exec-plans/tickets/*.md`
- fact-report の正本:
  - `docs/exec-plans/fact-reports/*.md`
- human-facing reference の補助 / summary docs:
  - `docs/references/*.md`
- reference band の本体 docs:
  - `docs/PRODUCT_SENSE.md`
  - `docs/DESIGN.md`
  - `docs/HUMAN_MANUAL.md`
  - `docs/exec-plans/active/attention-queue.md`
- 可視化:
  - `docs/exec-plans/canvas/development-flow.canvas`

`.canvas` は常に派生物であり、正本にはしない。

`docs/references/*.md` は補助 summary / hub docs の正本として扱ってよいが、`Product Sense`, `Design`, `Human Manual`, `Attention Queue` の reference band は本体 docs を直接入力として扱う前提で設計する。summary note を残す場合も従属 docs として扱い、band integrity の唯一条件にはしない。

## 移行中の互換 path
- source-of-truth はすでに `docs/exec-plans/` と `docs/references/` へ移した
- 旧 `planning/` や root `blocks/`, `chunks/`, `tickets/`, `canvas/`, `references/` は現行 source repo では使わない
- legacy layout を再現したい場合だけ `generation.planning_root = "."` などの明示 override を使う

## entity 一覧
- `block`
  - plan の中の高レベル実行単位
- `chunk`
  - block を実行可能単位へ分解した統合単位
- `ticket`
  - ワーカーが独立して完了できる最小単位

## ownership

### `block`
- 主担当:
  - `プランオーナー`
- 更新してよいもの:
  - `title`
  - `goal`
  - `status`
  - `depends_on`
  - `lane_order`
- 例外:
  - `タスクプランナー` は、配下最初の `chunk` を `in_progress` に上げる瞬間に限り、親 `block` の `pending -> in_progress` 同期だけ行ってよい
  - この例外は roll-up 整合のための status 同期だけに限る
  - `in_progress -> done`, `blocked`, `goal`, `depends_on`, `lane_order` は引き続き `プランオーナー` が判断する

### `chunk`
- 主担当:
  - `タスクプランナー`
- 更新してよいもの:
  - `title`
  - `status`
  - `parent_block`
  - `depends_on`
  - `lane_order`
  - chunk 内 ticket table

### `ticket`
- 主担当:
  - `タスクプランナー`
- 実行更新:
  - `タスクワーカー + reviewer`
- 更新してよいもの:
  - `status`
  - `assignee_role`
  - `editable_paths`
  - `depends_on`
  - `lane_order`
  - `fact-report` への参照

## status の許可値
- `pending`
- `in_progress`
- `done`
- `blocked`
- `obsolete`

## state transition

### `block`
- 許可:
  - `pending -> in_progress`
  - `in_progress -> done`
  - `in_progress -> blocked`
  - `blocked -> in_progress`
  - `pending -> obsolete`

### `chunk`
- 許可:
  - `pending -> in_progress`
  - `in_progress -> done`
  - `in_progress -> blocked`
  - `blocked -> in_progress`
  - `pending -> obsolete`

### `ticket`
- 許可:
  - `pending -> in_progress`
  - `in_progress -> done`
  - `in_progress -> blocked`
  - `blocked -> in_progress`
  - `pending -> obsolete`

## roll-up rules
- `block = done`
  - 配下 `chunk` はすべて `done`
  - 配下 `ticket` はすべて `done`
- `chunk = done`
  - 配下 `ticket` はすべて `done`
- `block = in_progress`
  - 少なくとも 1 つの配下 `chunk` が `in_progress` または `done`
- `chunk = in_progress`
  - 少なくとも 1 つの配下 `ticket` が `in_progress` または `done`
- `blocked` は上位へ自動伝播しない
  - 上位 role が判断して更新する

## done checklist rule
- `docs/exec-plans/blocks/*.md`, `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md` には `## Done チェック` を置く
- `status = done` に上げる前に、その note の checklist を更新する
- checklist は機械判定用ではなく、role が `done` へ移す根拠を明示するための人間向け根拠とする
- checklist が未整備でも parser は壊さないが、運用上は必須とみなす

## done 昇格権限
- `ticket`
  - `タスクワーカー + reviewer` が `Done チェック`、review 結果、`fact-report` を揃える
  - `タスクプランナー` が source docs sync を確認して `status = done` へ昇格させる
- `chunk`
  - `タスクプランナー` が `Done チェック` と chunk close 材料を揃える
  - `プランオーナー` が docs sync を確認して `status = done` へ昇格させる
- `block`
  - `プランオーナー` が `Done チェック` と配下整合を確認し、`status = done` へ昇格させる

## done 昇格前の同期
- `ticket = done` の前:
  - ticket 本文
  - `fact-report`
  - 関連 chunk の ticket table
  を同期する
- `chunk = done` の前:
  - chunk 本文
  - `chunk-close`
  - docs sync 対象
  を同期する
- `block = done` の前:
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/blocks/*.md`
  - 関連 chunk の status
  を同期する

`.canvas` sync はこれら source docs sync の後段に置く。

## commit cadence
- 既定の区切りは `ticket -> ticket -> ticket -> chunk` とする。
- `タスクワーカー`
  - 通常は ticket 完了ごとに commit を促さない。
  - 例外は、差分が大きい場合、危険な修正の場合、人間確認の直前の場合だけとする。
- `タスクプランナー`
  - chunk close、または複数 ticket の `done` 昇格と source docs sync をまとめた区切りで commit を提案する。
- `プランオーナー`
  - block 裁定や上流判断の差分は、必要なら独立 commit にしてよい。

## frontmatter schema

### block note
```md
---
block_id: BLK-001
parent_plan: PLAN-XXXX
title: 例
goal: この block が達成すること
status: pending
owner_role: plan_owner
depends_on: "-"
lane_order: 100
kind: block
---
```

### chunk note
```md
---
chunk_id: CHUNK-001
parent_plan: PLAN-XXXX
parent_block: BLK-001
title: 例
status: pending
owner_role: task_planner
depends_on: "-"
lane_order: 100
kind: chunk
---
```

### ticket note
```md
---
ticket_id: TICKET-001
parent_plan: PLAN-XXXX
parent_chunk: CHUNK-001
title: 例
status: pending
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - src/example
lane_order: 100
kind: ticket
---
```

### reference note
```md
---
reference_id: REF-EXAMPLE
title: Example
status: active
source_doc: docs/EXAMPLE.md
sync_mode: summary_mirror
owner_role: plan_owner
lane_order: 100
kind: reference
---
```

## role ごとの更新境界

### `プランオーナー`
- 更新対象:
  - `docs/exec-plans/project-intake.md`
  - `docs/exec-plans/discovery-brief.md`
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/blocks/*.md`
- 各 block の実装着手前に、人間へ仕様の聞き取りを行う責務を持つ
- 聞き取りと同時に、現時点で妥当な推奨案を提示する責務を持つ
- `chunk` / `block` の `done` 昇格判断を持つ
- 新しい `block` を追加したときは、`plan-spec` の block テーブルへ差し込む位置を同時に決める
- 大きな feedback、依存関係変更、途中追加 block が出たあとは、block 順序が依然として妥当かを再判定する
- block ごとの聞き取り項目には、必要に応じて実装言語、フレームワーク、設定方針、外部依存、テスト方針を含める
- 推奨案には、少なくとも 1 つのおすすめと、その理由を残す
- `block` を `done` にする前に `Done チェック` と source docs sync を確認する
- `docs/PRODUCT_SENSE.md`, `docs/DESIGN.md`, `docs/HUMAN_MANUAL.md` を更新したときは、残している `docs/references/*.md` の summary / hub の追従要否を判断する
- やらないこと:
  - chunk / ticket の詳細分解

### `タスクプランナー`
- 更新対象:
  - `docs/exec-plans/chunks/*.md`
  - `docs/exec-plans/tickets/*.md`
  - chunk 内 ticket table
- 例外的に更新してよいもの:
  - 配下最初の `chunk` を `in_progress` に上げるときだけ、親 `block` の `pending -> in_progress`
- `ticket` の `done` 昇格判断を持つ
- `chunk` を `done` にする前の `Done チェック` と docs sync 準備を持つ
- 各 ticket 完了時に、追加の chunk / ticket / block が必要かを再判定する
- `docs/exec-plans/active/attention-queue.md` を更新した場合は、残している `docs/references/attention-queue.md` の summary / hub の追従要否を判断する
- やらないこと:
  - 人間要求の再解釈
  - plan の目的変更
  - 親 `block` の `in_progress -> done`, `blocked`, `goal`, `depends_on`, `lane_order` の変更

### `タスクワーカー + reviewer`
- 更新対象:
  - ticket の `Done チェック`
  - ticket の `status`
  - `docs/exec-plans/fact-reports/*.md`
  - ticket 本文の事実欄
- `ticket` を `done` に上げる権限は持たず、`Done チェック` と review 結果を揃える
- 依存関係の変化でこの ticket 単体では進められないときは、`blocked` を使って上流へ戻す
- やらないこと:
  - `parent_block`
  - `parent_chunk`
  - chunk / block の goal 変更

## sync trigger
- `プランオーナー` が block を追加、削除、改名、status 変更したとき
- `タスクプランナー` が chunk / ticket を追加、削除、並び替え、status 変更したとき
- `タスクワーカー + reviewer` が ticket status を変えたとき
- reference band の本体 docs、active attention、または補助 `docs/references/*.md` を更新したとき

上記のいずれでも、最後に `obsidian-canvas-sync` を実行して `.canvas` を再同期する。

## validation rule
- `block_id`, `chunk_id`, `ticket_id` は一意
- `parent_block` は必ず `plan-spec` の block に存在する
- `parent_chunk` は必ず `docs/exec-plans/chunks/*.md` に存在する
- `lane_order` は同一親の下で重複してよいが、並びは昇順を基本とする
- frontmatter と本文 table の status が食い違う場合、frontmatter を正本とする
- reference band の primary input は本体 docs とし、band 用 metadata の正本契約は `docs/OBSIDIAN_CANVAS_SYNC.md` に従う
- `docs/references/*.md` を summary / hub note として残す場合は `reference_id`, `title`, `source_doc`, `sync_mode`, `owner_role`, `lane_order` を持つ
- `source_doc` は実在する docs を指し、`sync_mode` は `summary_mirror` か `runtime_summary` のどちらかにする

## generated attention queue 契約
- static queue seed の canonical source は docs 側に置き、generator code string を唯一正本にしない
- `AI案内可` は static item としてそのまま載せてよい
- `条件付き` は follow-up reminder としてだけ載せてよく、削除や採否を先回りして決めない
- `人間判断必須` は human review trigger としてだけ載せ、解決策や削除指示を静的文言へ埋め込まない

## migration 契約
- runtime artefact の正本は `docs/exec-plans/`、reference band の primary input は本体 docs として固定する
- `docs/references/*.md` は summary / hub / 補助 guide の層として扱い、band の唯一正本とはみなさない
- source repo 上でも generated repo 上でも、旧 root execution tree を再導入しない
- `migration` profile の docs は `docs/migration/` に残すが、実行中の planning artefact は `docs/exec-plans/` に寄せる

## 実装方針
- role skill はこの schema を前提に docs を更新する
- role skill は最後に `obsidian-canvas-sync` script を実行する
- 将来は validator script を追加し、sync 前に schema 不整合を検出する
