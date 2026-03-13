---
name: task-planner
description: plan-spec を chunk と ticket へ分解する skill。chunks と tickets を更新し、親子関係と lane order を整えたうえで最後に obsidian-canvas-sync script を実行する。
---

# Task Planner

`task-planner` は、plan を chunk / ticket へ分解し、既存 block 配下で閉じる follow-up を吸収しながら、chunk 完了まで同期する役割を持つ。

## 使う場面
- plan を chunk / ticket へ分解するとき
- 既存 block 配下で chunk / ticket の追加、削除、順序変更が必要なとき
- `task-worker` 完了後に ticket / chunk の status、table、handoff を同期するとき
- `promotion_candidates` や `sync_warnings` を見て、機械的に閉じられる ticket / chunk の同期漏れを解消するとき

## 最初に読む
- project の `docs/OPERATIONAL_SCHEMA.md`
- project の `docs/ROLE_SKILLS.md`
- 関連する `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/*.md`, `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md`, `docs/exec-plans/operator-requests/*.md`
- Obsidian canvas を使うなら `obsidian-canvas-sync` の skill。canonical source は `tools/codex-skills/obsidian-canvas-sync/SKILL.md`、export 済み repo では `.agents/skills/obsidian-canvas-sync/SKILL.md` でもよい

## 主担当
- `docs/exec-plans/chunks/*.md`
- `docs/exec-plans/tickets/*.md`
- `docs/exec-plans/operator-requests/*.md`
- chunk 内 ticket table
- 例外的に、配下最初の chunk を `in_progress` に上げる瞬間だけ、親 block の `pending -> in_progress` 同期

## 役割境界
- 人間要求や plan goal は変えない。plan 自体を変える必要があるなら `plan-manager` へ返す
- block に対して行える status 更新は、親 block の `pending -> in_progress` 同期だけ
- chunk が完了条件を満たし、source docs sync まで揃ったら、自分で `status = done` へ上げてよい
- block の `done`, `blocked`, `goal`, `depends_on`, `lane_order` 変更が必要なら `plan-manager` へ返す

## 必須成果
1. すべての chunk に正しい `parent_block` がある
2. すべての ticket に正しい `parent_chunk` がある
3. `ticket` は reviewer sign-off と source docs sync を確認してから `done` に上げる
4. `chunk` は `Done チェック`、chunk close 材料、source docs sync を確認してから `done` に上げる
5. `editable_paths`, `depends_on`, `lane_order` は `task-worker` が迷わない粒度で明示する
6. block の status 変更は、roll-up 整合のための `pending -> in_progress` 同期だけに限る
7. `Product Sense`, `Design`, `Human Manual`, `Attention Queue` は reference band の本体 docs として扱い、`docs/references/*.md` は残す場合だけ optional summary / hub として扱う
8. generated attention queue guidance は docs の `AI案内可 / 条件付き / 人間判断必須` 境界へ揃え、chunk / ticket 側で勝手に再解釈しない

## ticket 完了ごとの再判定
- 各 ticket が `done` になったら、次を必ず順に見る
  - 現 chunk の残 ticket をそのまま進められるか
  - 既存 block 配下で閉じる追加 chunk / ticket が必要か
  - pending operator request を chunk / ticket 追加で吸収できるか
  - block goal / 依存 / 順序の変更や human 裁定が必要か
- 既存 block 配下で閉じるなら、自分で追加 chunk / ticket を作ってよい
- block をまたぐ設計変更、人間裁定、goal 変更が必要な場合だけ `plan-manager` へ escalation する

## chunk close ルール
- 配下 ticket がすべて `done` でも、報告事項や未確認事項が同一 block 配下の追加 chunk / ticket で閉じられるなら、先にそれを生成してから現 chunk を閉じる
- 追加 follow-up が不要で、`Done チェック` と close 材料が揃っているなら、現 chunk を自分で `done` に上げる
- `promotion_candidates` に chunk が出ていて、必要な同期を自分で閉じられるなら `plan-manager` へ返す前に解消する
- chunk close 後に次 chunk を開ける必要があるなら、その handoff を同じターンで反映する

## commit cadence
- 既定 cadence は `ticket -> ticket -> ticket -> chunk`
- 毎 ticket ごとに commit を求めない
- chunk close、または複数 ticket の `done` 昇格と source docs sync をまとめた区切りで commit を提案する
- 大きな差分、危険な変更、人間 review 待ちのような例外だけ早めの commit 提案を検討する

## sync ルール
- `obsidian-canvas-sync` は `docs/exec-plans/chunks/`, `tickets/`, `operator-requests/` など source docs を更新したあとだけ実行する
- 可能なら `scripts/sync_canvas.py` を直接実行する
- schema が壊れているなら、先に docs を直してから sync する
- reference band や queue guidance の本体 docs も同ターンで変えた場合は、本体 docs を正として optional summary / hub の追従要否を判断する
