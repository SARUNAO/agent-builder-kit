---
block_id: BLK-004
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: GitHub 公開と配布導線を作る
goal: GitHub 上で mdBook と関連成果物を公開し、チュートリアルとして参照できる状態にする
status: pending
owner_role: plan_owner
depends_on: BLK-003
lane_order: 400
kind: block
---

# GitHub 公開と配布導線を作る

GitHub 上で mdBook を公開し、必要なら `agent-builder-kit` との関係も見える状態にする block。

## 想定スコープ
- GitHub repository / Pages の公開方針決定
- GitHub Actions による build / deploy
- `book.toml` の公開設定調整
- `agent-builder-kit` との配置関係や参照導線の整理

## 着手前の確認ポイント
- `agent-builder-kit` と mdBook を同一 repo に置くか、別 repo で相互参照するか
- GitHub Pages の project site 前提にするか
- 初回 publish から link check を必須にするか

## 推奨案
- 推奨: GitHub Pages を GitHub Actions で deploy し、mdBook 側は `site-url` など公開前提の設定を入れる
- 理由: GitHub の標準的な公開導線に乗せやすく、ワークショップ後の再配布もしやすい
- 代替案: 他ホスティングや手動 deploy も可能だが、再現性と保守性で不利

## Done チェック
- [ ] GitHub 上で公開された mdBook を参照できる
- [ ] build / deploy の自動化手順が docs と一致している
- [ ] `agent-builder-kit` との関係が README か本文で説明されている
