# ATTENTION Queue

「今は実装しないが、後で必ず再注目する事項」を管理する台帳。

## Active Items
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-2026-03-10-001 | closed | BLK-004 着手時 | `agent-builder-kit` と mdBook を同一 repo / 別 repo のどちらで公開するか決める | `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md` | 2026-03-10 | 2026-03-10 | 同一 repo で進める方針に確定 |
| ATN-2026-03-10-002 | closed | BLK-004 着手時 | link check や追加 lint を初回 publish から必須化するか判断する | `docs/exec-plans/discovery-brief.md`, `README.md` | 2026-03-10 | 2026-03-10 | 初回 publish では必須化せず、publish 後の改善項目として扱う |
| ATN-2026-03-10-003 | pending | TICKET-2026-03-10-031 実施時 | GitHub Pages の実公開 URL を README と本文へ反映する | `README.md`, `src/overview.md`, `src/conclusion.md` | 2026-03-10 | - | workflow 上の placeholder 解決とは別に、読者向け docs へ実 URL を入れる必要がある |
| ATN-2026-03-10-004 | pending | TICKET-2026-03-10-031 再開時 | GitHub repository を作成し、`origin` と push 先を設定して初回 publish を実行できる状態にする | `docs/exec-plans/tickets/ticket-2026-03-10-031-first-publish.md`, `README.md` | 2026-03-10 | - | 現在は remote 未設定かつ `gh` 未導入のため、publish 実行に入れない |

## Template
| id | status | trigger | required_action | source_links | opened_on | closed_on | notes |
|---|---|---|---|---|---|---|---|
| ATN-YYYY-MM-DD-XXX | pending | どの作業に入ったら再注目するか | 必須実装 / 必須確認事項 | 関連 docs へのリンク | YYYY-MM-DD | - | 補足 |
