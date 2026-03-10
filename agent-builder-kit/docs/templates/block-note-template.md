# Block Note Template

Obsidian `.canvas` や詳細メモ用に block を独立 note として持ちたいときの補助テンプレート。  
block の正本は `plan-spec` の `High-level blocks` テーブルであり、この note はそれを置き換えない。

```md
---
block_id: BLK-XXX
parent_plan: PLAN-YYYY-MM-DD-XXX
status: pending
title: {block title}
kind: block
---

# {block title}

## この block の役割
- 高レベルに何を達成する block か

## 着手前ヒアリング
- 人間へ確認したい実装論点
- 例:
  - 使用言語
  - フレームワーク
  - 設定方針
  - テスト方針

## `plan-manager` のおすすめ
- 第一候補
- 推す理由
- 主要な代替案との差分

## 関連する chunk
- CHUNK-XXX
- CHUNK-YYY

## Done チェック
- [ ] この block の goal が満たされている
- [ ] 関連する chunk がすべて `done`
- [ ] block 単位で残る未解決事項がない

## メモ
- plan-spec の表では書ききれない補足
```
