# Fact Report Template

下流から上流へ返す事実だけの報告。  
解釈や次の方針決定は上流側で行う。

```md
# Fact Report: {ticket title}

- ticket_id: TICKET-YYYY-MM-DD-XXX
- author: タスクワーカー
- submitted_on: YYYY-MM-DD

## 変更したファイル
- `path/to/file`

## 実行したコマンド
- `cargo test ...`
- `pnpm test ...`

## 結果
- 成功した検証
- 失敗した検証
- 未実施の検証

## reviewer 結果
- findings の有無
- 対応したかどうか

## 未解決事項
- 現時点で残っている事実ベースの懸念

## scope breach
- なし
- ある場合は、どこまで広がったか

## 補足
- 次 ticket に渡すべき事実
```
