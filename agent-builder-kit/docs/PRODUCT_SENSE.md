---
reference_id: REF-PRODUCT-SENSE
title: Product Sense
lane_order: 100
owner_role: plan_owner
sync_mode: direct_source
kind: reference_source
---

# Product Sense

## このプロジェクトは何か
- AI コーディング前提の開発フローを、毎回ゼロから考え直さずに初期化するための builder。
- 出力対象は `AGENTS.md` と、それに紐づく `docs/` 一式。
- 対象は新規作成プロジェクトと既存プロジェクトからの移行の両方。

## なぜ作るか
- AI 開発では、実装力より前に「どう分けて渡すか」「どの docs を正本にするか」で品質が大きくぶれる。
- 現行プロジェクト A では運用実績がある一方、責務集中や docs 配置の改善余地が見えた。
- 改善案 B はあるが、次のプロジェクトごとに人手で移植するのは重い。
- そこで C では、A/B を抽象化し、再利用可能な開発フローの工場ラインを作る。

## 誰のためか
- AI エージェントを複数役で運用する開発者
- 新規リポジトリの初期セットアップを早く済ませたい人
- 既存プロジェクトに docs 駆動の開発フローを後付けしたい人

## 価値
- 役割分担、docs 構造、進捗更新ルールを初日から揃えられる
- task 分解と review の粒度を固定しやすい
- プロジェクトごとの差異は入力として受け、フローの骨格は共通化できる

## 非目的
- すべての開発文化を 1 つの型へ強制すること
- 特定言語や特定フレームワーク専用の scaffold を作ること
- ドメイン仕様そのものを自動生成すること

## reference summary との分担
- この file は reference band の本体 docs として扱う
- `docs/references/product-sense.md` は optional summary / hub として残してよい
- summary を残す場合も、canvas band の代替正本にはしない
- 本体には背景、対象ユーザー、価値、非目的の説明を残す
- summary には短い見取り図だけを置き、全文コピーにしない
