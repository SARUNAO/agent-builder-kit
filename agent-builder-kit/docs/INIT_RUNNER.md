# Init Runner

この docs は、`docs-builder.toml` を読んで初期 skeleton を生成する `init_runner` の責務を定義する。

## 結論
- `init_runner` は置く
- ただし責務は `bootstrap` に限定する
- 日々の status 更新、done 昇格、review 判断は持たせない

## 役割
- `docs-builder.toml` を読む
- profile / packs に応じて初期ファイル群を生成する
- role skill と `.canvas` の初期配置までを行う
- 初期 block を seed して、運用開始地点を作る

## role skill bundle 契約
- generated repo へは少なくとも以下を出力する
  - canonical:
    - `plan-manager`
    - `task-planner`
    - `task-worker`
    - `reviewer`
  - support:
    - `obsidian-canvas-sync`
  - inventory:
    - `tools/codex-skills/README.md`
  - user-facing export:
    - `.agents/skills/README.md`
- `agent-builder-kit` 自体は `tools/codex-skills/` の canonical bundle だけを同梱し、`.agents/skills/` は generated repo 生成時にだけ出力してよい
- `task-worker` は code ticket 完了後に `reviewer` へ handoff する前提で配る
- markdown / docs 主体 ticket は docs-only skip を許すが、skip 条件は runtime docs に明示して使う

## `conductor` backport 後の bootstrap / export
- `conductor` を package へ同梱する場合、skill 正本は `tools/codex-skills/conductor/`、runtime asset 正本は `tools/conductor/` を使う
- `init_runner` は generated repo 作成時に、skill docs の export だけでなく、必要な runtime asset も生成先へ複製する前提で扱う
- generated repo では利用者向け入口として `.agents/skills/` を出力してよいが、package 自体は `tools/` 配下の canonical source を正本とする
- current repo 固有の `docs/article-instrumentation/` や tutorial 本文は bootstrap 対象に含めない

## 持たせるもの
- `AGENTS.md`
- `README.md`
- `docs/`
- `docs/HUMAN_MANUAL.md`
- `tools/codex-skills/`
- `.agents/skills/`
- `docs/references/`
- `docs/exec-plans/canvas/development-flow.canvas`
- 初期 `docs/exec-plans/plan-spec.md`
- 初期 `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/` の雛形

## 持たせないもの
- 日々の progress 更新
- `done` 昇格判定
- reviewer 判定
- chunk close 運用
- `.canvas` を source of truth とすること
- generic package 利用時に、builder 自身の active queue や in-flight plan を持ち込むこと

## 2 層モデル

### 1. bootstrap schema
- `docs-builder.toml`
- 何を生成するかを決める

### 2. runtime schema
- `OPERATIONAL_SCHEMA.md`
- 生成後にどう運用するかを決める

`init_runner` は前者だけを扱い、後者は role skill が扱う。

## 推奨 bootstrap フロー
1. `docs-builder.toml` を読む
2. profile と packs を解決する
3. `AGENTS.md` と core docs を生成する
4. role skill bundle を配置する
   - code review 用の `reviewer` も canonical asset として配置する
   - package asset の正本は `tools/codex-skills/` に置く
   - generated repo では利用者向け export として `.agents/skills/` へ mirror する
   - `conductor` を同梱する場合は、skill docs を `tools/codex-skills/conductor/`、runtime asset を `tools/conductor/` から出力する
5. `docs/exec-plans/` と `docs/PLANS.md` を空の generic seed へ初期化する
6. `docs/references/` の seed を生成する
7. `project.mode = "migration"` のときは `docs/migration/` を生成し、現行 AI 向け依頼文も置く
8. 初期 `docs/exec-plans/plan-spec.md` と `docs/exec-plans/blocks/`, `docs/exec-plans/chunks/`, `docs/exec-plans/tickets/` の雛形を置く
9. `.canvas` を初回生成する

generic bootstrap では、builder 固有の queue や progress の現在値をそのまま持ち込まず、package docs に置いた cluster 名ベースの static queue seed と空の progress seed を使う。
builder 自身の履歴を引き継ぐのは `self_hosting_pack` など明示条件のときだけとする。

## 目立つ入口
- migration pack 有効時は、ルートに `MIGRATION_START_HERE.md` を置く
- これは現行 AI に最初に見せる入口で、`docs/migration/current-ai-migration-request.md` へのリンクだけを短く強く置く
- 依頼本文の正本は引き続き `docs/migration/current-ai-migration-request.md`
- 入口ではまず `Step 1` だけを案内し、棚卸し結果を返させてから次へ進める

## 初期 block seed

### 目的
- 新規プロジェクトでは、最初から実装 block を決め打ちしない
- まず `プランオーナー` が人間に聞き取りを行う入口を作る

### 既定の block
- `BLK-001`
  - title: `何を作るか決める`
  - goal:
    - 人間要求を聞き取り、最初の実装可能 block 群を定義する
  - status:
    - `pending`

### 意味
- この block は discovery 専用の seed block として扱う
- `プランオーナー` はこの block を起点に
  - `project-intake`
  - `discovery-brief`
  - `plan-spec`
  を更新しながら、後続 block を追加する

## migration 時の初期 block seed

### 既定の block
- `BLK-001`
  - title: `現行運用を棚卸しする`
  - goal:
    - 既存 docs、受け渡し、保護 path を整理し、新 schema への写像方針を定義する
  - status:
    - `pending`

### 意味
- migration では、いきなり実装 block を切らず、まず現行運用の inventory を取る
- `プランオーナー` は `docs/migration/project-inventory.md` と `current-ai-migration-request.md` を起点に現行 AI へ調査を依頼する

## 理想の運用
- 初期化直後:
  - `.canvas` には `何を作るか決める` block が 1 つある
- その後:
  - `プランオーナー` が人間へ聞き取りを行う
  - block を追加する
  - `タスクプランナー` が chunk / ticket を生やす
  - 開発フロー全体が後から形成される

つまり、`init_runner` は完成済みのフローを吐くのではなく、フローを育てるための最初の足場を吐く。

## references seed
- `obsidian_canvas_pack` が有効なときは、上段中央 band 用に初期 `docs/references/` を生成する
- 既定候補:
  - `PRODUCT_SENSE`
  - `DESIGN`
  - `attention-queue`
  - `human-manual`

## 初回確認ポイント
- `docs/index.md` から core docs と execution docs に辿れること
- target contract では `docs/exec-plans/plan-spec.md` と `docs/exec-plans/blocks/` に seed が生成されること
- `docs/exec-plans/active/attention-queue.md` が package docs 正本から読まれた cluster 名ベースの static seed で始まること
- `docs/exec-plans/completed/progress-log.md` が空 seed で始まること
- `tools/codex-skills/` に `reviewer` を含む canonical role skill bundle が生成されること
- `.agents/skills/` に同じ skill bundle が export され、利用者向け入口として読めること
- code ticket は `task-worker` 後に reviewer を呼び、docs-only ticket は skip 条件を明示して運用できること

## smoke test
- clean workspace bootstrap の最低限確認は `python3 tests/test_clean_workspace_smoke.py`
- この test は temp workspace へ `agent-builder-kit` を展開し、`generated/` への bootstrap 成功と最小成果物の存在を確認する
- skill 配置と主要リンクの整合確認は `python3 tests/test_validation_checks.py`
- この test は source repo / generated repo では canonical + export、`agent-builder-kit` では canonical-only 配置と主要 relative link を確認する
- profile / pack 差分の smoke は `python3 tests/test_profile_pack_smoke.py`
- この test は temp workspace で `standard + obsidian_canvas_pack`, `migration_pack + obsidian_canvas_pack`, `self_hosting_pack + obsidian_canvas_pack` を回し、pack ごとの追加 doc と非追加 doc を確認する
- `agent-builder-kit` 単体でも `self_hosting_pack` が失敗せず、`AGENTS.md` / `README.md` は package 内 source がなくても generic fallback で生成できることを確認する

## 移行中の実装メモ
- 現行コードの既定出力は `docs/exec-plans/` と `docs/references/` に追従している
- legacy path を使う場合だけ manifest override を明示する
- したがってこの docs は target contract を示し、現行実装との差分は migration 対象として扱う

## 最小出力の考え方
- `minimum`
  - role skill と core docs のみ
- `standard`
  - `minimum` + planning templates + 初期 seed block
- `expanded`
  - `standard` + add-on packs + reference band
- `self_hosting_pack`
  - builder 自身のメタ docs を source から引き継ぐ

## 実装形
- 想定ファイル:
  - `tools/init_runner.py`
- 入力:
  - `docs-builder.toml`
  - 雛形はルート `docs-builder.toml.example`
- 出力:
  - 生成された初期 skeleton 一式

## 現在の実装
- 実装ファイル:
  - `tools/init_runner.py`
- 実行例:
  - `python3 tools/init_runner.py docs-builder.toml`
  - `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml`
  - `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml --cleanup-package`
- 利用入口:
  - `README.md`
  - `docs/DOCS_BUILDER_TOML.md`
- `conductor` backport 後の検証では、package canonical source を更新したうえで `python3 agent-builder-kit/tools/init_runner.py docs-builder.toml` のような package 起点の bootstrap を再度確認する
- migration pack 有効時:
  - `MIGRATION_START_HERE.md`
  - `docs/migration/index.md`
  - `docs/migration/project-inventory.md`
  - `docs/migration/gap-report.md`
  - `docs/migration/adoption-plan.md`
  - `docs/migration/current-ai-migration-request.md`
  を生成する

## package cleanup 分岐
- 既定では展開元の `agent-builder-kit/` は削除しない
- `--cleanup-package` を付けたときだけ、`agent-builder-kit/tools/init_runner.py` から実行している場合に限って `agent-builder-kit/` 自体を削除する
- source repo の `tools/init_runner.py` では `--cleanup-package` を付けても削除しない
- 生成先が `agent-builder-kit/` の内側にある危険な構成では cleanup を skip する
- 実運用では、init 後に AI が人間へ「展開元 package を残すか削除するか」を確認し、削除判断が出たときだけ cleanup を使う

## 次の実装論点
- `docs-builder.toml` に bootstrap 専用 section を切るか
- 初期 seed block を常に 1 個だけにするか
- migration pack の文面をどこまで manifest から具体化するか
