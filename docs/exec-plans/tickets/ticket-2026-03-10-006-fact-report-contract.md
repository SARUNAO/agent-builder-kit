---
ticket_id: TICKET-2026-03-10-006
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
parent_chunk: CHUNK-2026-03-10-003
title: `fact-report` と記録ルールを揃える
status: done
owner_role: task_planner
assignee_role: task_worker
editable_paths:
  - docs/templates/fact-report-template.md
  - README.md
  - docs/HUMAN_MANUAL.md
lane_order: 200
depends_on: TICKET-2026-03-10-005
kind: ticket
---

# `fact-report` と記録ルールを揃える

- ticket_id: TICKET-2026-03-10-006
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- parent_chunk: CHUNK-2026-03-10-003
- status: done
- owner_role: task_planner
- assignee_role: task_worker
- lane_order: 200
- last_updated: 2026-03-10

## Goal
- `fact-report` と補助 docs に、一次記録へ渡す最低限のルールを埋め込む

## やること
- `fact-report` template に decision / gotcha / command / before-after を返しやすい欄を追加する
- `README.md` や `docs/HUMAN_MANUAL.md` に、記録の残し方を短く追記する
- docs-only 変更でも何を一次記録へ返すか分かるようにする

## やらないこと
- 各 ticket の実例ログ記入
- mdBook 本文の執筆
- review 契約の意味変更

## Editable Paths
- `docs/templates/fact-report-template.md`
- `README.md`
- `docs/HUMAN_MANUAL.md`

## Inputs
- TICKET-2026-03-10-005 で作った記録 docs
- 既存の `fact-report` template

## Implementation Notes
- 事実と解釈は分離したままにする
- 記録を要求しすぎて worker の負荷が上がりすぎないようにする

## Verification
- template を読むだけで、何を返せば記録 block が助かるか分かる
- README / Human Manual と template の説明が矛盾しない

## Done When
- 後続 ticket が統一された粒度で一次記録を返せる

## Done チェック
- [x] Goal を満たす更新が入っている
- [x] Verification を実施して結果を残した
- [x] docs-only skip または reviewer sign-off の扱いを明記した
- [x] 未解決事項があれば `fact-report` に記録した

## Auto Review
- 使用する review skill: reviewer
- reviewer に見てほしい観点: 記録ルールが過剰でも不足でもないか

## 完了時に返すもの
- `fact-report`
- 追加した記録項目の一覧
- 運用上の懸念

## 実施結果
- `docs/templates/fact-report-template.md` に、`decision / gotcha / command / before-after` へ再利用しやすい欄と書き方の目安を追加した
- `README.md` に BLK-007 以降の記録ルールを追記した
- `docs/HUMAN_MANUAL.md` に、人間が確認すべき一次記録の粒度を追記した
- この ticket は markdown / docs 更新のみなので reviewer は docs-only skip とする

## Verification 結果
- template を読むだけで、`結果` と `記録素材メモ` の使い分けが分かる状態にした
- README と Human Manual に同じ記録ルールを短く反映した

## Fact Report
- `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-006-fact-report-contract.md`
