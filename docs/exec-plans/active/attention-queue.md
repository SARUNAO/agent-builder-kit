# ATTENTION Queue

「今は実装しないが、後で必ず再注目する事項」を管理する台帳。

## Active Items
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-2026-03-10-001 | pending | BLK-004 着手時 | `agent-builder-kit` と mdBook を同一 repo / 別 repo のどちらで公開するか決める | `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md` | 2026-03-10 | - | 公開導線と GitHub Pages 設計に影響する |
| ATN-2026-03-10-002 | pending | BLK-004 着手時 | link check や追加 lint を初回 publish から必須化するか判断する | `docs/exec-plans/discovery-brief.md`, `README.md` | 2026-03-10 | - | 初回は `mdbook build` を最低ゲートにして進めている |

## Template
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-YYYY-MM-DD-XXX | pending | どの作業に入ったら再注目するか | 必須実装 / 必須確認事項 | 関連 docs へのリンク | YYYY-MM-DD | - | 補足 |
