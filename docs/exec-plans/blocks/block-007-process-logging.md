---
block_id: BLK-007
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: 開発ログと記事素材の記録基盤を整える
goal: 実際の開発作業を後から客観的に記事化できるよう、一次記録の置き場と記録ルールを固める
status: done
owner_role: plan_owner
depends_on: BLK-002
lane_order: 250
kind: block
---

# 開発ログと記事素材の記録基盤を整える

作業中の判断、コマンド、詰まり、差分を一次資料として残し、後続の章作成で根拠として使えるようにする block。

## 確認済み事実
- この mdBook の主題には、実際の開発プロセスそのものが含まれる
- あとからチュートリアル化するには、作業時点の客観的な記録が必要である
- すでに plan / chunk / ticket / progress-log などの planning docs は存在する
- BLK-002 の実例として、導入判断、章構成、build / serve の記録がすでに発生している
- いま必要なのは、本文より先に一次記録の置き場と書き方を固定することである
- root `asset/` に補助スナップショットが追加され、本文補助素材として再利用できる候補が増えた

## 想定スコープ
- decision log の置き場
- gotcha log の置き場
- command log の置き場
- before / after で見せる差分の残し方
- `fact-report` と本文素材の関係整理

## この block で採用する前提
- 記録 docs はまず `docs/exec-plans/` 配下へ寄せる
- 一次記録は command / decision / gotcha / before-after を最小単位にし、全文ログやスクリーンショットを必須にしない
- 公開時は内部判断をそのまま全文公開するのではなく、本文では要約を正とし、必要な根拠だけ一次記録から引く
- どの判断を公開向けに要約し直すかは publish block で最終確認する

## 推奨案
- 推奨: 最初は `decision log`, `gotcha log`, `command log`, `before/after` の 4 系統を docs と fact-report で運用し、本文は後からそれを参照して書く
- 理由: 事実と読者向けの説明を分離でき、あとで章へ再配置しやすい
- 主な代替案: 本文作成と同時に記録も書く案はあるが、その時点の判断と後付けの解釈が混ざりやすい

## Done チェック
- [x] 一次記録の置き場が決まっている
- [x] 記録ルールが後続 ticket で運用できる粒度に落ちている
- [x] BLK-003 が記録を根拠として本文作成へ進める

## 完了メモ
- `docs/exec-plans/active/` に `decision-log`, `gotcha-log`, `command-log`, `before-after`, `article-source-map` を整備した
- `fact-report` template と README / Human Manual に、一次記録を返す最小ルールを反映した
- BLK-002 の実例を retro 収集し、初期 4 章ごとに根拠と不足記録を整理した
- root `asset/` の補助スナップショットは、内容断定ではなくファイル名ベースの補助素材として素材マップへ取り込んだ
