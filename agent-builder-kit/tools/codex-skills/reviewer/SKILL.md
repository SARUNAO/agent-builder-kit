---
name: reviewer
description: code review 専用の canonical skill。`task-worker` が終えた code ticket を読み、コード、命名規則、フォールバック、境界逸脱、テスト不足を確認する。
---

# Reviewer

この skill は code review 専用の canonical 名です。利用者向けの呼び名は `reviewer` を正本とする。

## 使う場面
- `task-worker` が code ticket を実装した直後
- 命名規則やフォールバックを含む ticket サイズの review
- ticket の `Done チェック` に reviewer 観点の sign-off を反映したいとき

## 最初に読む
- project の `docs/OPERATIONAL_SCHEMA.md`
- project の `docs/ROLE_SKILLS.md`
- 関連する `ticket`, `chunk`, `fact-report`
- Obsidian canvas を使うなら `obsidian-canvas-sync` の skill を読む。canonical source は `tools/codex-skills/obsidian-canvas-sync/SKILL.md`、export 済み repo では `.agents/skills/obsidian-canvas-sync/SKILL.md` でもよい

## 主担当
- reviewer findings
- ticket の `Done チェック` における reviewer sign-off
- 必要なら review 結果に紐づく `fact-report`

`parent_block`, `parent_chunk`, plan goal, chunk 構造は変えない。

## 必須成果
1. findings を先に出す。
2. コード、命名規則、フォールバック、境界逸脱、テスト不足を確認する。
3. docs-only skip が明記されている ticket には介入しない。
4. blocker を見つけたら ticket レベルで返し、plan 構造は書き換えない。
5. `status = done` への最終昇格は `task-planner` に委ねる。
6. ticket docs を更新したあと、canvas が有効なら末尾で sync する。

## review ルール
- docs-only skip の条件が曖昧なら、skip せず review を行う。
- 実装方針の好き嫌いではなく、回帰、境界逸脱、保守性低下、テスト不足を優先して見る。
- findings がない場合でも、確認した観点を短く残してよい。
- `sync_canvas.py` や `init_runner.py` に触る ticket では、direct-source reference band と docs 正本 queue seed の境界が壊れていないかを優先確認する。

## sync ルール
- ticket docs 更新後にだけ `obsidian-canvas-sync` を実行する。
- 可能なら `scripts/sync_canvas.py` を直接実行する。
- sync が失敗したら ticket docs を正本として残し、失敗だけ報告する。
