---
block_id: BLK-003
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: ワークショップ章を作る
goal: agent-builder の流れを体験できる章構成と本文を作成する
status: pending
owner_role: plan_owner
depends_on: BLK-002
lane_order: 300
kind: block
---

# ワークショップ章を作る

mdBook 骨格の上に、参加者が role フローを追体験できる章を載せる block。

## 想定スコープ
- 章構成の最終決定
- 各章の本文ドラフト
- 参加者向けの操作手順や期待結果

## 着手前の確認ポイント
- 章数を最小 3 章にするか、role 説明込みで 4 章以上にするか
- agent-builder の説明を独立章にするか、各章へ分散するか

## 推奨案
- 推奨: 「概要」「環境確認」「role フロー体験」「最初の変更」の 4 章構成を骨格にし、増える内容は章内目次で吸収する
- 理由: mdBook と agent-builder の両方を過不足なく見せやすく、将来の追加にも耐えやすい
- 代替案: 3 章に圧縮する案は短くできるが、role ごとの責務説明が薄くなりやすい

## Done チェック
- [ ] 章構成が人間確認済みである
- [ ] 章ごとの役割と期待結果が曖昧でない
