---
block_id: BLK-004
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: GitHub 公開と配布導線を作る
goal: GitHub 上で mdBook と関連成果物を公開し、チュートリアルとして参照できる状態にする
status: in_progress
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
- GitHub Pages を project site として出す場合の repository 名と公開 URL をどう置くか
- GitHub Actions の最小ゲートを `mdbook build` だけにするか、追加確認をどこまで入れるか

## 推奨案
- 推奨: GitHub Pages を GitHub Actions で deploy し、mdBook 側は `site-url` など公開前提の設定を入れる
- 理由: GitHub の標準的な公開導線に乗せやすく、ワークショップ後の再配布もしやすい
- 代替案: 他ホスティングや手動 deploy も可能だが、再現性と保守性で不利

## この turn で確定した方針
- `agent-builder-kit` と mdBook は同一 repo で公開する
- 公開先は GitHub Pages を使う
- 初回 publish の最小ゲートは `mdbook build` とし、link check は publish 後の改善項目として扱う
- `agent-builder-kit` はすでに repo ルート下へ配置済みの前提で進める

## plan-manager メモ
- BLK-004 の前提は固まったため、次は `task-planner` で GitHub Pages / GitHub Actions / README 導線 / `book.toml` 調整を chunk / ticket へ分解できる

## task-planner メモ
- 2026-03-10: 先頭 chunk を `in_progress` に上げたため、roll-up 整合として BLK-004 も `in_progress` に同期した

## Done チェック
- [ ] GitHub 上で公開された mdBook を参照できる
- [ ] build / deploy の自動化手順が docs と一致している
- [ ] `agent-builder-kit` との関係が README か本文で説明されている
