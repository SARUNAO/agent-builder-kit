---
block_id: BLK-005
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: 運用導線と仕上げを整える
goal: README、Human Manual、必要な補助 docs を更新し、再開しやすいワークショップ状態にする
status: pending
owner_role: plan_owner
depends_on: BLK-004
lane_order: 500
kind: block
---

# 運用導線と仕上げを整える

ワークショップを途中再開しやすくし、参加者が次に何を読むべきか迷わないようにする block。

## 想定スコープ
- README の更新
- `docs/HUMAN_MANUAL.md` や関連 docs の導線調整
- 必要なら公開手順や次の拡張候補の整理

## 着手前の確認ポイント
- 参加者向け説明と開発者向け説明をどこまで分けるか
- 公開済み mdBook への導線をどこに集約するか

## 推奨案
- 推奨: 再開手順、役割導線、公開済み成果物への入口を README と Human Manual に集約する
- 理由: repo を開いた人が、実装参加と閲覧の両方で迷いにくくなる
- 代替案: 説明を各所へ分散する案は柔軟だが、入口が散らばりやすい

## Done チェック
- [ ] README と運用 docs の役割分担が明確である
- [ ] 初回ワークショップ後に次の block へ進める導線が残っている
