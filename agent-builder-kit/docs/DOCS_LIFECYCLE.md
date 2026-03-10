# Docs Lifecycle

この docs は、開発 phase ごとに「主に見る docs」と「主導線から外してよい docs」を整理する memo。

`deprecated` は削除を意味しない。
ここでは「その phase を越えたら、常時見なくてよい docs」を指す。

## Phase 1: Onboarding

### 主に見る docs
- `../README.md`
- `index.md`
- `HUMAN_MANUAL.md`
- `INIT_RUNNER.md`
- `DOCS_BUILDER_TOML.md`
- `BOOTSTRAP_LAYOUT.md`

### この phase の目的
- builder をどう起動するか分かる
- どの agent に何を頼むか分かる
- runtime artefact の置き場が分かる

### phase を越えたら主導線から外してよい docs
- `INIT_RUNNER.md`
- `DOCS_BUILDER_TOML.md`
- `BOOTSTRAP_LAYOUT.md`

## Phase 2: Active Development

### 主に見る docs
- `exec-plans/plan-spec.md`
- `exec-plans/blocks/`
- `exec-plans/chunks/`
- `exec-plans/tickets/`
- `exec-plans/active/attention-queue.md`
- `exec-plans/canvas/development-flow.canvas`
- `HUMAN_MANUAL.md`
- `ROLE_SKILLS.md`

### この phase の目的
- block -> chunk -> ticket の順で進める
- `task-planner` が ticket close / chunk close の再計画判断を行う
- attention-queue に送るべき deferred item を見落とさない

### この phase では常時見なくてよい docs
- `INIT_RUNNER.md`
- `DOCS_BUILDER_TOML.md`
- `BOOTSTRAP_LAYOUT.md`

## Phase 3: Release Readiness

### 主に見る docs
- `ACCEPTANCE_MATRIX.md`
- `HUMAN_MANUAL.md`
- `../README.md`
- `index.md`

### この phase の目的
- package 単体で入口が自己完結しているか確認する
- smoke / profile-pack 差分を確認する
- 初見利用者が迷わない導線になっているか確認する

### release 前に再注目する docs
- `INIT_RUNNER.md`
- `OUTPUT_PROFILES.md`
- `BOOTSTRAP_LAYOUT.md`
- `HUMAN_MANUAL.md`

## 運用ルール
- docs を自動削除しない
- 主導線から外すかどうかは人間が決める
- block が 1 つ進んだら、この memo を見て入口 docs の優先度を見直してよい
- release 前には onboarding で使った docs を再点検する
