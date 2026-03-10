# Current AI Migration Request Template

現行プロジェクトを担当している AI に渡す依頼文の叩き台。  
目的は「既存 docs をそのまま壊さず、新 schema への写像案を作ること」であって、即座の置換ではない。

```md
# Migration Request For Current AI

あなたはこのプロジェクトの現行 docs / 運用を把握している AI です。  
以下の migration bootstrap を参照し、既存運用を新 schema へ写像してください。

## 目的
- 既存運用を棚卸しし、新しい docs schema へ安全に移行する
- いきなり上書きせず、差分と導入順を明確にする

## 参照するもの
- `docs/migration/project-inventory.md`
- `docs/migration/gap-report.md`
- `docs/migration/adoption-plan.md`
- `docs/OPERATIONAL_SCHEMA.md`
- `docs/ROLE_SKILLS.md`
- 必要なら `docs/OBSIDIAN_CANVAS_SYNC.md`

## 進め方
### Step 1
- 既存 docs と運用 artefact を棚卸しし、`project-inventory` を埋める
- この step が終わったら、まだ次の step を実行せず、棚卸し結果を返す

### Step 2
- `project-inventory` を元に、現在の flow を `block / chunk / ticket` 相当へ写像する
- 新 schema と噛み合わない点を `gap-report` に書く
- この step が終わったら、差分と open question を返す

### Step 3
- `gap-report` を元に、段階的な導入順を `adoption-plan` に書く
- 人間承認が必要な判断と protected path を明示する
- この step が終わったら、導入 plan を返す

## 禁止事項
- 既存 docs をいきなり正本から外さない
- 人間承認なしで破壊的な rename / delete をしない
- `.canvas` を source of truth にしない

## 返してほしいもの
- Step 1 完了時: 埋まった `project-inventory`
- Step 2 完了時: 埋まった `gap-report`
- Step 3 完了時: 埋まった `adoption-plan`
- 残っている open question
```
