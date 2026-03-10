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
- human-facing reference の正本:
  - `docs/references/*.md`
- human-facing reference の意味上の本体 docs:
  - `docs/PRODUCT_SENSE.md`
  - `docs/DESIGN.md`
  - `docs/HUMAN_MANUAL.md`
  - `docs/exec-plans/active/attention-queue.md`
- 可視化:
  - `docs/exec-plans/canvas/development-flow.canvas`

`.canvas` は常に派生物であり、正本にはしない。

`docs/references/*.md` は canvas band が直接読む正本だが、`summary view` として本体 docs への案内責務も持つ。reference note 単体を意味上の唯一正本として扱わない。

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
  - `タスクプランナー` は、配下の最初の chunk を `in_progress` または `done` に上げる時に限り、roll-up 整合のため親 block の `pending -> in_progress` を同期してよい

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

## in_progress 同期権限
- `ticket`
  - `タスクワーカー` が実装着手時に `pending -> in_progress` へ上げてよい
- `chunk`
  - `タスクプランナー` が着手中の実態に合わせて `pending -> in_progress` を反映してよい
- `block`
  - 原則は `プランオーナー` が `pending -> in_progress` を判断する
  - ただし `タスクプランナー` は、配下 chunk の着手により roll-up 上すでに進行中とみなせる場合に限り、親 block の `pending -> in_progress` を同期してよい
  - この例外は status の意味変更ではなく、既存計画の実行開始を source docs に反映するための整合更新として扱う

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
- `docs/PRODUCT_SENSE.md`, `docs/DESIGN.md`, `docs/HUMAN_MANUAL.md` を更新したときは、対応する `docs/references/*.md` の summary も current context と一致しているか確認する
- やらないこと:
  - chunk / ticket の詳細分解

### `タスクプランナー`
- 更新対象:
  - `docs/exec-plans/chunks/*.md`
  - `docs/exec-plans/tickets/*.md`
  - chunk 内 ticket table
- `ticket` の `done` 昇格判断を持つ
- `chunk` を `done` にする前の `Done チェック` と docs sync 準備を持つ
- 配下 chunk の着手に伴う roll-up 整合として、親 block の `pending -> in_progress` 同期を行ってよい
- 各 ticket 完了時に、追加の chunk / ticket / block が必要かを再判定する
- `docs/exec-plans/active/attention-queue.md` を更新した場合は、`docs/references/attention-queue.md` の summary も current attention と一致しているか確認する
- やらないこと:
  - 人間要求の再解釈
  - plan の目的変更
  - block の `done` / `blocked` 昇格判断

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
- 本体 docs または active attention の変更で対応する `docs/references/*.md` を更新したとき

上記のいずれでも、最後に `obsidian-canvas-sync` を実行して `.canvas` を再同期する。

## validation rule
- `block_id`, `chunk_id`, `ticket_id` は一意
- `parent_block` は必ず `plan-spec` の block に存在する
- `parent_chunk` は必ず `docs/exec-plans/chunks/*.md` に存在する
- `lane_order` は同一親の下で重複してよいが、並びは昇順を基本とする
- frontmatter と本文 table の status が食い違う場合、frontmatter を正本とする
- reference note は `reference_id`, `title`, `source_doc`, `sync_mode`, `owner_role`, `lane_order` を持つ
- `source_doc` は実在する docs を指し、`sync_mode` は `summary_mirror` か `runtime_summary` のどちらかにする

## migration 契約
- runtime artefact の正本は `docs/exec-plans/`、reference band の正本は `docs/references/` として固定する
- source repo 上でも generated repo 上でも、旧 root execution tree を再導入しない
- `migration` profile の docs は `docs/migration/` に残すが、実行中の planning artefact は `docs/exec-plans/` に寄せる

## 実装方針
- role skill はこの schema を前提に docs を更新する
- role skill は最後に `obsidian-canvas-sync` script を実行する
- 将来は validator script を追加し、sync 前に schema 不整合を検出する
