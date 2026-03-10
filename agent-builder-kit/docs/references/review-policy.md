# レビュー方針

## 目的
- task review と chunk review の役割重複を避ける
- review の粒度を固定して、重要な findings を埋もれさせない

## Task Review

### 対象
- 1 ticket の差分

### 観点
- バグ
- 回帰
- 境界逸脱
- 検証不足
- ticket 契約違反

### 出力
- findings
- open questions
- ticket 完了可否

## Chunk Review

### 対象
- 2-5 ticket をまとめた統合状態

### 観点
- task 間の接続不整合
- 命名や責務のねじれ
- docs 同期漏れ
- commit 単位として妥当か
- 次 chunk へ進める前提が揃っているか

### 出力
- findings
- 統合リスク
- docs sync 要否
- commit ready 可否

## ルール
- task review は必須
- chunk review も必須
- 同じ指摘を 2 回繰り返さない
- task review で落ちた ticket は chunk に含めない
- chunk review で plan 前提が崩れたら `プランマネージャー` へ戻す

## Skill 化の境界
- `task-review skill`
  - ticket 差分をレビューする
- `chunk-close skill`
  - chunk review、docs 同期、commit 前確認を束ねる

## reviewer の入力
- ticket
- fact-report
- 差分
- 直近の関連 ticket
- chunk-sheet

## reviewer の出力
- findings first
- 重要度順
- no-finding の場合も明記
