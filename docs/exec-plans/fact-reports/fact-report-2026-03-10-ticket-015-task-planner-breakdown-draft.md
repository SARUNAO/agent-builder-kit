# Fact Report: `task-planner で仕事を chunk と ticket に分ける` 章の本文ドラフトを作る

- ticket_id: TICKET-2026-03-10-015
- author: タスクワーカー
- submitted_on: 2026-03-10

## 変更したファイル
- `src/SUMMARY.md`
- `src/role-flow.md`
- `docs/exec-plans/chunks/chunk-2026-03-10-008-task-planner-breakdown.md`
- `docs/exec-plans/tickets/ticket-2026-03-10-015-task-planner-breakdown-draft.md`

## 実行したコマンド
- `sed -n '1,220p' docs/exec-plans/chunks/chunk-2026-03-10-008-task-planner-breakdown.md`
- `sed -n '1,260p' docs/exec-plans/tickets/ticket-2026-03-10-015-task-planner-breakdown-draft.md`
- `sed -n '1,260p' src/role-flow.md`
- `sed -n '1,220p' src/SUMMARY.md`
- `sed -n '1,220p' docs/exec-plans/chunks/chunk-2026-03-10-001-mdbook-bootstrap.md`
- `sed -n '1,220p' docs/exec-plans/chunks/chunk-2026-03-10-002-mdbook-verification.md`
- `sed -n '1,220p' docs/exec-plans/tickets/ticket-2026-03-10-001-mdbook-prereq.md`
- `sed -n '1,220p' docs/exec-plans/tickets/ticket-2026-03-10-002-mdbook-init.md`
- `mdbook build`
- `python3 .agents/skills/obsidian-canvas-sync/scripts/sync_canvas.py --plan-spec docs/exec-plans/plan-spec.md --block-dir docs/exec-plans/blocks --chunk-dir docs/exec-plans/chunks --ticket-dir docs/exec-plans/tickets --reference-dir docs/references --vault-root . --canvas docs/exec-plans/canvas/development-flow.canvas`

## 結果
- `src/role-flow.md` を、`task-planner` の役割、使い方、chunk / ticket の分け方を説明する草稿へ差し替えた
- `src/SUMMARY.md` の章ラベルを `task-planner で仕事を chunk と ticket に分ける` に更新した
- `BLK-002` を `CHUNK-001`, `CHUNK-002` と `TICKET-001` から `TICKET-004` に分けた実例を本文へ取り込んだ
- 配下 ticket 完了後に chunk を更新 / 追加する判断と、block 単位へ戻す判断を本文へ追記した
- `src/images/before_chunk.png` と `src/images/after_chunk.png` を、更新前後の chunk イメージとして本文に組み込んだ
- 着手実態に合わせて `CHUNK-008` と `TICKET-015` を `in_progress` に更新した
- `mdbook build` は成功した
- `.canvas` の再同期は成功した

## 記録素材メモ
- decision:
  - 抽象的な `role フロー体験` ではなく、`task-planner` の役割と使い方が一目で分かる章タイトルへ寄せた
  - 章の説明は一般論だけでなく、実際に作成済みの chunk / ticket を使う構成にした
- gotcha:
  - 章ファイル名はまだ `role-flow.md` のままだが、本文と `SUMMARY.md` の章タイトルはすでに `task-planner` 主題へ切り替わっている
  - canvas sync script は `--plan-spec` などの明示引数が必要だった
- command:
  - `mdbook build` で章タイトル変更と本文差し替え後も book が生成できることを確認した
- before / after:
  - before: role 分担を短く示すだけのプレースホルダだった
  - after: `task-planner` の入力、出力、分解基準、chunk 再編判断、`task-worker` への handoff を説明する草稿になった

## reviewer 結果
- docs-only skip
- 理由: markdown / docs 更新のみで、コードパスや設定値の変更がないため

## 未解決事項
- `task-planner` を実際に呼び出したプロンプト例は 1 本だけ入れているため、後続推敲で別 block の再分解例を追加する余地がある
- `src/role-flow.md` というファイル名を章タイトルに合わせて変更するかは、後続 chunk 全体の命名とあわせて再判断してよい

## scope breach
- あり
- 利用者の指示に合わせて、`task-worker` 実行前に `CHUNK-008` を `pending -> in_progress` へ同期した

## 補足
- 次の `TICKET-016` では、本文の言い回しと source map の同期を整えながら、必要なら章タイトルや小見出しをさらに詰める
