# Chunk Close Template

chunk 完了時の包括レビュー、docs 同期、commit 判断をまとめる。  
`タスクプランナー` と `reviewer`、必要に応じて `プランマネージャー` が使う。

```md
# Chunk Close: {chunk title}

- chunk_id: CHUNK-YYYY-MM-DD-XXX
- parent_plan: PLAN-YYYY-MM-DD-XXX
- status: pending_review
- owner: タスクプランナー
- last_updated: YYYY-MM-DD

## 含まれる ticket
- TICKET-001
- TICKET-002

## 受領した fact-report
- FACT-TICKET-001
- FACT-TICKET-002

## Task Review 集約
- 各 ticket の review 結果
- 未解決 findings の有無

## Chunk Review 結果
- findings
- integration_risks
- commit_ready: yes | no

## docs sync 対象
- 更新が必要な docs
- 根拠

## commit 単位の判断
- 今回まとめてよい差分
- 分けるべき差分

## 次 chunk への引き継ぎ
- 残件
- 新しく開く ticket
- 人間判断が必要な事項

## close 条件
- chunk review の重大 findings が解消済み
- docs sync 対象が整理済み
- commit 単位が確定済み
```
