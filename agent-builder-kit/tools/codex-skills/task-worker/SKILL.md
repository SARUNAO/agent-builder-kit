---
name: task-worker
description: ticket 単位の実装を扱う canonical skill。ticket status と fact-report を更新し、コード編集があるときは reviewer へ handoff する。
---

# Task Worker

この skill は実装担当の canonical 名です。review は `reviewer` へ分離し、利用者向けの実装入口は `task-worker` に一本化する。

## 使う場面
- ticket の実行
- ticket 進捗の docs 反映

## 最初に読む
- project の `docs/OPERATIONAL_SCHEMA.md`
- 関連する `ticket`, `chunk`, `editable_paths`
- Obsidian canvas を使うなら `obsidian-canvas-sync` の skill を読む。canonical source は `tools/codex-skills/obsidian-canvas-sync/SKILL.md`、export 済み repo では `.agents/skills/obsidian-canvas-sync/SKILL.md` でもよい

## 主担当
- ticket の `Done チェック`
- ticket の `status`
- ticket 本文の事実欄
- `fact-report`

`parent_block`, `parent_chunk`, plan goal, chunk 構造は変えない。

## 必須成果
1. `editable_paths` の範囲に留まる。
2. plan の再解釈ではなく事実を報告する。
3. コード編集がある ticket では、実装後に `reviewer` へ handoff する。
4. markdown / docs 主体 ticket は docs-only skip を明示したうえで reviewer を省略してよい。
5. blocker が見つかったら plan 構造を書き換えず ticket レベルで `blocked` を付けて上流へ返す。
6. ticket を `done` に上げない。最終昇格は `task-planner` に渡す。
7. ticket status が変わり canvas が有効なら最後に sync する。
8. reference band や generated attention queue に関わる ticket では、本体 docs と docs 正本を先に更新し、`docs/references/*.md` や generator code string を唯一正本として扱わない。

## commit 運用
- 通常は、ticket 完了ごとに commit を促さない。
- 既定の区切りは chunk 単位であり、commit 提案は原則 `task-planner` 側へ寄せる。
- 例外として、次の場合だけ早めの commit を提案してよい。
  - 差分が大きい
  - 危険な修正で切り戻ししやすさを優先したい
  - 人間確認の直前で履歴固定の価値が高い
- 上記に当たらない限り、ticket を終えた時点では未コミットのまま次 ticket へ進んでよい。

## sync ルール
- ticket docs 更新後にだけ `obsidian-canvas-sync` を実行する。
- 可能なら `scripts/sync_canvas.py` を直接実行する。
- sync が失敗したら ticket docs を正本として残し、失敗だけ報告する。
- optional summary / hub docs の更新は、その ticket の editable_paths に明示されているときだけ行う。
