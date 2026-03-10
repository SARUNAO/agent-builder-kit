# Project Intake Template

人間から受けた要求原文を崩さずに保持する入口 docs。  
標準では `プランオーナー`、拡張時は `仕様設計者` が主担当。

```md
# Project Intake: {request title}

- intake_id: INTAKE-YYYY-MM-DD-XXX
- related_plan: PLAN-YYYY-MM-DD-XXX
- status: captured
- owner: プランオーナー
- requested_on: YYYY-MM-DD
- last_updated: YYYY-MM-DD

## 要求原文
- ユーザーの依頼を、解釈せずそのまま残す

## 依頼から読み取れること
- 作りたいもの
- 想定していそうな利用場面
- 明らかに不足している情報

## まず確認すべき論点
- 成果物の種類
- 対象ユーザー
- MVP の範囲
- データソースや制約

## block 着手前の仕様確認メモ
- ここでは block 実装に入る直前の追加ヒアリング候補を残す
- 例:
  - 使用言語
  - 開発フレームワーク
  - 設定ファイルや環境変数の扱い
  - テスト / lint / review の期待値
  - 外部サービスやデータ保存の前提

## 初期おすすめ
- 現時点でのおすすめ案
- 採用理由
- 主要な代替案と trade-off

## 初期リスク
- 要求が曖昧
- 外部依存が重い
- 運用コストが不明

## 次アクション
- `discovery-brief` を起こす
- 人間へ確認を返す
- block ごとの追加ヒアリングが必要かを仮置きする
```
