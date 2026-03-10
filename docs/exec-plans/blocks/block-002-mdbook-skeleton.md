---
block_id: BLK-002
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: mdBook の最小骨格を作る
goal: `book.toml` と `src/` の最小構成を作り、ローカル build 可能な状態にする
status: pending
owner_role: plan_owner
depends_on: BLK-001
lane_order: 200
kind: block
---

# mdBook の最小骨格を作る

BLK-001 で確定した方針に従い、mdBook の最小構成を作る block。

## 想定スコープ
- `mdbook` 導入手順または前提確認
- `book.toml`
- `src/SUMMARY.md`
- 章ファイルの最小雛形
- build / serve 確認に必要な最小手順

## 着手前の確認ポイント
- `mdbook` をローカル導入するか、ワークショップ内で導入手順を再現するか
- `mdbook init` 後の雛形をどこまで残し、どこから workshop 向けに差し替えるか

## 推奨案
- 推奨: 公式ガイドに沿って `mdbook init` で骨格を作り、`mdbook serve --open` と `mdbook build` を最初の受け入れ条件にする
- 理由: 初回導入時の手順ミスを減らしつつ、公式ドキュメントに沿った再現性を保てる
- 代替案: 手動で最小ファイルを作る案は学習には良いが、初回のワークショップ素材としては立ち上がりが遅くなりやすい

## Done チェック
- [ ] 最小構成の受け入れ条件が BLK-001 の確認結果と整合している
- [ ] `mdbook` 導入有無と導入手順が利用者向けに説明可能である
- [ ] 後続の章作成 block が必要とする前提ファイルが定義されている
