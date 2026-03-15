---
reference_id: REF-HUMAN-MANUAL
title: Human Manual
lane_order: 400
owner_role: plan_owner
sync_mode: direct_source
kind: reference_source
---

# Human Manual

## 目的
- 人間がどこで判断し、どこから AI に任せるかを明確にする
- `plan-manager`, `task-planner`, `task-worker`, `reviewer` をどう使い分けるかを固定する
- canvas を見ながら block -> chunk -> ticket の順で開発を進められるようにする

## 最初に見る場所
- 入口:
  - `../README.md`
  - `index.md`
- 実行中の flow:
  - `exec-plans/plan-spec.md`
  - `exec-plans/canvas/development-flow.canvas`
- role 契約:
  - `ROLE_SKILLS.md`
- release 前確認:
  - `ACCEPTANCE_MATRIX.md`

## package 単体利用時の最短手順
1. `../README.md` を開く
2. `HUMAN_MANUAL.md` を開く
3. `plan-manager` にやりたいことと追加要件を伝える
4. `task-planner` に chunk / ticket を切ってもらう
5. `exec-plans/canvas/development-flow.canvas` を見ながら `task-worker` に進めてもらう

## `conductor` backport 後の見方
- `conductor` runtime asset を同梱したあとは、script 実体を `tools/conductor/`、skill 本文を `tools/codex-skills/conductor/` のように分けて見る
- package の canonical source を更新したあと、generated repo へどのように届くかの手順は `INIT_RUNNER.md` を正本として確認する
- generated repo では利用者向け入口が `.agents/skills/` に mirror されることがあるが、package 自身の正本配置は引き続き `tools/` 配下で確認する

## backport 後の確認順
1. `tools/conductor/` に runtime asset がそろっているかを見る
2. `tools/codex-skills/` に `conductor` を含む skill docs があるかを見る
3. `INIT_RUNNER.md` の bootstrap / export 手順どおりに generated repo へ反映されるか確認する
4. generated repo では `.agents/skills/` の mirror と runtime asset の配置が崩れていないかを見る

## `conductor` を package 単体で使うときの読み方
- `conductor` は same-block bounded multi-step を正として使う
- 既定値は `LEVEL=MID step=5`
- override が必要なら、自然文より次の準正規形を優先して書く
  - `LEVEL=MID step=5`
  - `LEVEL=HIGH step=20`
- `HIGH` や大きい step を指定しても無制限にはならない
  - hard stop
  - `plan_manager` 返送
  - reviewer handoff 必須
  - active block 変更
  - 実効 step 上限到達
  で止まる
- `MID` は package 利用者向けの既定 level として読む
  - active ticket / chunk がある間は same-block bounded multi-step を進める
  - active block だけが残り、次に必要なのが chunk / ticket 生成なら `task_planner` への narrow handoff も含めてよい
- `HIGH` はその `MID` を含んだ上位 level として読む
  - block close-ready 段階では `plan_manager` 返送を優先する
- code ticket 後段の reviewer は direct target ではなく internal role として扱う
  - no-findings path: `reviewer_pass_through.triggered = true`
  - finding あり path: `reviewer_pass_through.blocking = true`, `next_role = task_worker`
- `.agents/skills/` が存在しても export mirror として扱い、正本確認は `tools/codex-skills/` と `tools/conductor/` を優先する

## 人間が最終判断すること
- 何を作るか、何を作らないか
- 優先順位
- 要求の採否
- protected path を変更してよいか
- role model や pack の採用可否
- block を増やすか、既存 block に吸収するか
- `blocked` の解除条件
- release へ進めてよいか

## AI に任せてよいこと
- inventory の初回ドラフト
- gap の洗い出し
- block / chunk / ticket の起票と更新
- 実装と検証
- fact-report の記録
- `.canvas` の同期

## role ごとの頼み方

### `plan-manager` に頼むこと
- やりたいことを伝える
- block に入る直前の仕様を煮詰めてもらう
- 言語、フレームワーク、設定、pack、依存、テスト方針のおすすめを出してもらう
- 大きな feedback や追加要件が出たときに、新 block を足すか、既存 block に吸収するか判断してもらう
- block 完了時に `done` 昇格してよいか判断してもらう

### `task-planner` に頼むこと
- block を chunk に分けてもらう
- chunk を ticket に分けてもらう
- 依存関係、`blocked`、順序を整理してもらう
- ticket 完了後に `done` に上げてよいか判断してもらう
- ticket 完了のたびに、新しい chunk / ticket / block が必要か再判定してもらう
- chunk 完了時に、新しい chunk を切る必要があるか判断してもらう
- 行き詰まりや懸念点が出たときに、既存 chunk で吸収するか、新しい chunk を作るか判断してもらう

### `task-worker` に頼むこと
- ticket の実装
- docs 更新、コード変更、検証実行
- fact-report の記録
- 実装後に `task-planner` へ `done` 判断を渡すところまで

### `reviewer` に頼むこと
- コード編集を伴う ticket の後段 review
- コード、命名、fallback、境界逸脱、テスト不足の確認
- docs-only ticket では skip してよい

## 標準の進め方

### 1. まず `plan-manager` に目的を伝える
- 例:
  - 何を改善したいか
  - どこに違和感があるか
  - 追加したい機能や要件は何か
- この段階で `plan-manager` に仕様確認とおすすめを出してもらう

### 2. block を決める
- 既存 block に入れるか、新 block を足すかを `plan-manager` に判断してもらう
- 追加 feedback が大きいときは、末尾追加ではなく差し込み位置も確認する
- canvas 上で block の順序が妥当かも見る

### 3. `task-planner` に chunk / ticket を切ってもらう
- block を chunk に分ける
- 実装単位を ticket に分ける
- `depends_on` と `lane_order` を揃える
- `blocked` が必要なら明示してもらう

### 4. `task-worker` に ticket を実行してもらう
- 1 ticket ずつ進める
- 実装が終わったら、検証結果と fact-report を残してもらう
- コード編集ありなら後段で `reviewer` を通す

### 5. `task-planner` に `done` 判断をしてもらう
- ticket の Goal が閉じているか
- follow-up ticket が必要なら切るか
- 既存 chunk の中で吸収するか、新 chunk / 新 block に逃がすか

### 6. chunk が終わったら次の塊を判断してもらう
- chunk の Goal が閉じているか
- 懸念点や未解決事項を次の ticket で足すだけでよいか
- まとまりとして新しい chunk を作るべきか
- block 自体を分けるべきか

### chunk close で `task-planner` に確認してもらうこと
- 含まれる ticket がすべて `done` か
- chunk の Goal が閉じているか
- 未解決事項は follow-up ticket で足せるか、新 chunk が必要か
- block へ戻して再設計すべき論点がないか
- `attention-queue` に pin すべき deferred item があるか
- canvas 上の status と docs の status が一致しているか
- `plan-manager` に block close 判断を渡せる状態か

## attention-queue に入れるもの
- 今すぐ実装しないが、後で必ず再注目しないと危険な事項
- 明確な `trigger` を持つ事項
- release 前、特定 ticket 着手時、特定 block close 時のように再注目タイミングを言える事項
- その場では閉じないが、忘れると契約や品質を壊す事項

## attention-queue に入れないもの
- 単なる改善アイデア
- 次の ticket を切れば十分な未解決事項
- 既存 chunk の中でそのまま扱える残件
- いつ再注目するか決まっていない曖昧なメモ

## 迷ったときの使い分け
- すぐ次に実装するなら ticket にする
- まとまりとして続きがあるなら chunk を切る
- 今は着手しないが、再注目しないと危険なら attention-queue に入れる

### 7. canvas を見ながら次へ進む
- block -> chunk -> ticket の順で進める
- 今どこが `in_progress` か
- `blocked` がどこにあるか
- 次にやる ticket は何か
- reference band の内容が現状とずれていないか

## canvas の見方
- block:
  - 開発の大きな段階
- chunk:
  - block の中のまとまり
- ticket:
  - 実装や docs 更新の最小単位
- reference band:
  - Product Sense, Design, Attention Queue, Human Manual の要約

`.canvas` は可視化であり、正本は docs。
判断に迷ったら `docs/exec-plans/` と `docs/references/` を正として読む。

## 差し戻しが必要な場面
- 仕様が固まっていないまま実装に入りそうなとき
- 追加要求が出たのに、既存 ticket へ無理に押し込もうとしているとき
- 追加要求や懸念点が、既存 chunk の粒度を越えているとき
- root / package / generated の 3 面同期が崩れたとき
- canvas の進捗と docs の status がずれたとき
- `blocked` にすべきなのに `pending` や `in_progress` のまま進めようとしているとき

## `blocked` の考え方
- 前提が未確定で、その ticket 単体では閉じられないときに使う
- follow-up ticket を切れば元 ticket が閉じられるなら、`blocked` ではなく `done`
- 迷ったら `task-planner` に、新規 ticket で吸収できるかを判断してもらう

## release 前に人間が確認すること
- `ACCEPTANCE_MATRIX.md` の command が通っているか
- `README.md`, `docs/index.md`, `HUMAN_MANUAL.md` の導線が初見利用者に通じるか
- package 単体でも入口 docs が自己完結しているか
- reference band が placeholder に戻っていないか
- `Human Manual` と `README.md` が初見の利用者に通じるか

## migration 時の追加確認
- 現行 AI が `MIGRATION_START_HERE.md` か `docs/migration/current-ai-migration-request.md` を起点に動いているか
- Step 1, Step 2, Step 3 を一度にやらせず、段階ごとに返却させているか
- `docs/migration/project-inventory.md` が埋まっているか
- `docs/migration/gap-report.md` に open question が残っているか
- `docs/migration/adoption-plan.md` に段階導入 plan があるか

## 原則
- 既存 docs をいきなり破棄しない
- AI に丸投げしてもよいが、禁止事項と返却物は明示する
- `.canvas` は可視化であり、正本は docs
- status 更新後は canvas sync まで含めて 1 セットで考える

## reference summary との分担
- この file は reference band の本体 docs として扱う
- `docs/references/human-manual.md` は optional summary / hub として残してよい
- summary を残す場合も、canvas band の代替正本にはしない
- 本体には判断責務、承認ポイント、差し戻し条件、進め方、release 前確認を残す
- summary には短い見取り図だけを置き、詳細ルールは本体に残す
