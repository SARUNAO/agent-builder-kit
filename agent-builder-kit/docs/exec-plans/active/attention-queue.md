# ATTENTION Queue

「今は実装しないが、後で必ず再注目する事項」を管理する台帳。

## ルール
- 新規の後回し事項は、このファイルへ 1 行追加する。
- 実装開始時に `trigger` と現在タスクを照合し、該当すれば宣言する。
- 完了時は `status` を `done` にし、`closed_on` を埋める。

## Active Items
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| まだなし | - | - | - | - | - | - | generic package は空 seed で開始する。 |

## Template
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-YYYY-MM-DD-XXX | pending | どの作業に入ったら再注目するか | 必須実装 / 必須確認事項 | 関連 docs へのリンク | YYYY-MM-DD | - | 補足 |
