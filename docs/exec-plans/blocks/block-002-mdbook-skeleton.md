---
block_id: BLK-002
parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
title: mdBook の最小骨格を作る
goal: `book.toml` と `src/` の最小構成を作り、ローカル build 可能な状態にする
status: done
owner_role: plan_owner
depends_on: BLK-001
lane_order: 200
kind: block
---

# mdBook の最小骨格を作る

BLK-001 で確定した方針に従い、mdBook の最小構成を作る block。

`CHUNK-2026-03-10-001` と `CHUNK-2026-03-10-002` が完了し、導入前提整理、最小骨格生成、初期 4 章、build / serve 確認まで到達した。

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
- [x] 最小構成の受け入れ条件が BLK-001 の確認結果と整合している
- [x] `mdbook` 導入有無と導入手順が利用者向けに説明可能である
- [x] 後続の記録 block と章作成 block が必要とする前提ファイルが定義されている

## 完了メモ
- `mdbook v0.5.2` を導入し、`book.toml`, `src/SUMMARY.md`, `src/*.md` の最小構成を作成した
- 初期章は「概要」「環境確認」「role フロー体験」「最初の変更」の 4 章で仮置きした
- `mdbook build` は成功した
- `mdbook serve --open` は通常ローカル環境では起動確認し、sandbox では localhost bind 制約があることを確認した
- README に初学者向けの build / serve 手順を反映した
