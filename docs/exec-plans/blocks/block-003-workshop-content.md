---
block_id: BLK-003
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: ワークショップ章を作る
goal: 一次記録を踏まえて、`agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングを主軸にした章構成と本文を作成する
status: done
owner_role: plan_owner
depends_on: BLK-007
lane_order: 300
kind: block
---

# ワークショップ章を作る

mdBook 骨格と一次記録の上に、参加者が `agent-builder-kit` の開発フローと、その土台にある docs 駆動開発 / ハーネスエンジニアリングを追体験できる章を載せる block。

## 想定スコープ
- 章構成の最終決定
- `agent-builder-kit` と docs 駆動開発を主題にした編集方針
- 各章の本文ドラフト
- 参加者向けの操作手順や期待結果
- やわらかめのチュートリアル文体への寄せ方

## 着手前の確認ポイント
- mdBook 入門と `agent-builder-kit` tutorial の比重をどう置くか
- `agent-builder-kit` の説明を独立節にするか、各章へ分散するか
- `ハーネスエンジニアリング` を用語のまま出すか、補足つきで噛み砕くか
- 一次記録をそのまま章に埋め込むか、解説文として再構成するか
- 文体をどこまでやわらかくし、どこまで planning docs の厳密さを残すか

## 推奨案
- 推奨: 章構成は 4 章骨格を維持しつつ、比重は mdBook 3、`agent-builder-kit` / 開発フロー 7 程度へ寄せる
- 推奨: 「ようこそ、Agent-builder-kit のチュートリアルへ」くらいのやわらかさを許容しつつ、各章の根拠は一次記録へ戻れる形を保つ
- 推奨: mdBook は成果物例として扱い、主題は `AGENTS.md` と docs 構成でどう開発が進んだかへ置く
- 理由: この repo の独自性は mdBook 単体ではなく、`agent-builder-kit` と docs 駆動フローを実地でどう運用したかにあるため
- 代替案: mdBook 入門を前面に出す案は導入しやすいが、`agent-builder-kit` tutorial としての密度が下がりやすい

## この turn で確定した方針
- mdBook を前面に出しすぎず、`agent-builder-kit` tutorial を主軸にする
- 比重は mdBook 3、`agent-builder-kit` / 開発フロー 7 を目安にする
- 文体は planning docs の硬さ 10 に対して 7 程度を目安にし、少し歓迎文を入れてよい
- ただし根拠リンクと事実の粒度は、現在の docs 運用を崩さない
- 章タイトルは仮置きとし、本文の推敲や章の役割整理に応じて動的に変更してよい

## Done チェック
- [x] 章構成が人間確認済みである
- [x] 章ごとの役割と期待結果が曖昧でない
- [x] 本文の主張が一次記録と矛盾していない

## 完了メモ
- `はじめに` から `おわりに` までの本文系 chunk がすべて `done` になった
- mdBook より `agent-builder-kit` と docs 駆動フローを前面に出す方針で、全 chapter の役割を固めた
- Obsidian 導入ガイドの後追い追加も含め、source map と本文の根拠同期が完了した
- 次 block の GitHub 公開は、repo 配置関係や Pages 方針の確認が残るため `pending` のまま plan-owner 聞き取りへ渡す
