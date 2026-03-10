---
block_id: BLK-001
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: 初期スコープと公開方針を固める
goal: 現状事実、公開ゴール、推奨方針を整理し、後続 block の前提を確定する
status: done
owner_role: plan_owner
depends_on: "-"
lane_order: 100
kind: block
---

# 初期スコープと公開方針を固める

環境構築済み / mdBook 本体未着手という現状を整理し、公開まで見据えた後続 block の前提を固める block。

## 確認済み事実
- planning workspace と canvas は生成済み
- mdBook の本体ファイルはまだ存在しない
- これから作るべき対象は mdBook ワークショップ記事サイトである
- ゴールは GitHub で `agent-builder-kit` と mdBook を公開し、ワークショップまたはチュートリアルとして機能する状態まで含む
- `agent-builder-kit` は現在この repo 直下にない
- 2026-03-10 時点では `mdbook` コマンドが利用できない

## 採用した前提
- mdBook の初期化は `mdbook init` を第一候補にする
- ローカル確認は `mdbook serve --open` を使う
- 必須品質ゲートは `mdbook build` を基準にし、Rust コード例を入れたら `mdbook test` を追加する
- 公開は GitHub Pages と GitHub Actions を第一候補にする
- 章数は 3 から 4 章程度を初期骨格とし、必要なら章内目次で拡張する
- ワークショップの主眼は agent-builder の role フロー体験に置く

## 後続 block へ持ち越す確認事項
- GitHub 上で `agent-builder-kit` と mdBook を同一 repo / 別 repo のどちらで公開するか
- 公開時に link check を必須化するか
- `agent-builder-kit` をいつ、どの形でこの workspace に持ち込むか

## 推奨案
- 推奨: 先に公式推奨の mdBook 最小骨格を起こし、その上で GitHub Pages 公開へつなぐ
- 理由: 導入・ローカル確認・公開の責務を block ごとに分けやすい
- 主な代替案: 初手で repo 構成や公開先を完全確定する案もあるが、まだ本体がない段階では判断材料が薄い

## Done チェック
- [x] 要求原文が `project-intake` に整理されている
- [x] `discovery-brief` に確認済み事実、仮置き前提、未確定事項、推奨案が分離されている
- [x] 後続の実装 block が `plan-spec` に追加されている
- [x] 人間確認が必要な論点が block note に明示されている
