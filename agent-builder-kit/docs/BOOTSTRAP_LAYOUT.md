# Bootstrap Layout

この docs は、`agent-builder` の package assets と bootstrap 後の runtime artefact の境界を定義する。

## 結論
- runtime artefact の正本は `docs/exec-plans/` に置く
- reference band の正本は本体 docs に置き、`docs/references/` は optional summary / hub として扱う
- root 直下には `README.md`, `AGENTS.md`, `docs/`, `tools/`, `docs-builder.toml` を基本として残す
- `agent-builder-kit/` は source repo や一時展開では存在し得るが、生成先 repo の恒久構成には含めない
- `docs-builder.toml` は保持を既定とし、`agent-builder-kit/` は残してもよいが不要なら人間が手動削除する

## 現在の配置

### root に残すもの
- `README.md`
- `AGENTS.md`
- `docs/`
- `tools/`
- `docs-builder.toml`

### `docs/` 配下に置くもの
```text
docs/
├── index.md
├── PLANS.md
├── PRODUCT_SENSE.md
├── DESIGN.md
├── HUMAN_MANUAL.md
├── references/
│   ├── index.md
│   ├── product-sense.md
│   ├── design.md
│   ├── attention-queue.md
│   └── human-manual.md
├── exec-plans/
│   ├── project-intake.md
│   ├── discovery-brief.md
│   ├── plan-spec.md
│   ├── blocks/
│   ├── chunks/
│   ├── tickets/
│   ├── fact-reports/
│   ├── active/
│   ├── completed/
│   └── canvas/
└── migration/
```

## 判断基準
- `blocks` / `chunks` / `tickets` / `fact-reports` / `canvas` は同じ execution lifecycle に属するため、`docs/exec-plans/` の同じ親配下へ集約する
- reference band は `docs/PRODUCT_SENSE.md`, `docs/DESIGN.md`, `docs/HUMAN_MANUAL.md`, `docs/exec-plans/active/attention-queue.md` を direct source として使う
- `docs/references/` は optional summary / hub として残してよく、band の唯一正本にはしない
- source asset と generated artefact を root で混在させない

## source repo と generated repo の区別

### source repo にだけ残るもの
- `agent-builder-kit/`
- editor / vault 固有の local file

### generated repo に残したいもの
- root: `README.md`, `AGENTS.md`, `docs/`, `tools/`, `docs-builder.toml`
- `docs/exec-plans/` 配下の execution artefact
- `docs/references/` 配下の human-facing reference

## 後続 ticket との関係
- `TICKET-013` で `init_runner` の既定出力は `docs/exec-plans/` と `docs/references/` に追従済み
- `TICKET-014` で source repo 上の planning artefact, reference tree, canvas path を新トポロジーへ物理移行する
- `TICKET-015` で `agent-builder-kit/` は任意保持、`docs-builder.toml` は保持既定という cleanup 契約を確定した
