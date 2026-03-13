---
name: conductor
description: package 同梱の `flow_conductor.py` を読み、MID では 1 block を終わらせる側の既定 bounded multi-step、HIGH では block close-ready の plan-manager 返送まで含む上位 bounded multi-step で downstream role skill を既定 5 step、override 時は指定 step まで進める orchestration skill。
---

# Conductor

この skill は package 利用時の human-facing 入口です。`tools/conductor/flow_conductor.py` の判定を読み、`MID` では 1 block を終わらせる側の既定 bounded multi-step、`HIGH` ではその `MID` を含んだまま block close-ready の `plan_manager` 返送まで含む上位 bounded multi-step で進めます。

## 使う場面
- human が `conductor` だけを入口として呼びたいとき
- current state から bounded に進めたいとき
- hard stop や advisory を見たうえで downstream role を選びたいとき

## 最初に読む
- project の `docs/OPERATIONAL_SCHEMA.md`
- project の `docs/ROLE_SKILLS.md`
- project の `docs/HUMAN_MANUAL.md`
- `docs/exec-plans/plan-spec.md`
- 必要なら active な `block` / `chunk` / `ticket`

## 実行入口
- current state の取得:
  - `python3 tools/conductor/flow_conductor.py --human`
- 必要なら isolated state で確認:
  - `python3 tools/conductor/flow_conductor.py --human --runtime-state-dir /tmp/<任意ディレクトリ>`
- execution override を明示するとき:
  - `python3 tools/conductor/flow_conductor.py --human --level HIGH --max-steps 20`

## human 向け override 記法
- human は自然文完全自由入力ではなく、次の準正規形を優先して書く
  - `LEVEL=MID step=5`
  - `LEVEL=HIGH step=20`
- skill はこの指定を読めた場合、内部では `--level` と `--max-steps` に正規化して runtime へ渡す
- 省略時既定は `LEVEL=MID`, `step=5`

## この skill がやること
1. `flow_conductor.py` を実行して `stop_reason`, `dispatchable`, `route_hint`, `reviewer_pass_through`, `close_ready_handoff`, `advisories`, `promotion_candidates`, `sync_warnings`, `bounded_multi_step` を読む
2. `stop_reason != null` なら downstream skill を起動せず、人間へ停止理由と次 role を返す
3. `dispatchable = false` なら downstream skill を起動せず、人間へ返す
4. `reviewer_pass_through.triggered = true` かつ `blocking = false` なら、bounded run の internal role として `reviewer` を起動する
5. それ以外で `dispatchable = true` かつ `route_hint` が次のいずれかなら、対応する skill を実行する
   - `task_planner` -> `task-planner`
   - `task_worker` -> `task-worker`
   - `plan_manager` は返送境界なので、この bounded run では自動起動しない
6. downstream skill 実行後は、active block が変わらず・`stop_reason = null`・`dispatchable = true`・reviewer finding による blocking が無く・step 数が `bounded_multi_step.max_steps_per_run` 未満なら、`flow_conductor.py` を再実行して次 step を判定する
7. 次のどれかに当たったら、その turn を止めて人間へ返す
   - `route_hint = plan_manager`
   - `stop_reason != null`
   - `dispatchable = false`
   - `reviewer_pass_through.blocking = true`
   - active block 変更
   - step 数が `bounded_multi_step.max_steps_per_run` に達した

## やらないこと
- source docs の直接更新
- `done` 昇格
- block の goal / depends_on / lane_order 変更
- `reviewer` の直接起動
- reviewer direct dispatch
- unlimited な block 横断自動ループ

## 解釈ルール
- `route_hint`
  - runtime の出力をそのまま使う
  - skill 本文側で再計算しない
- `close_ready_handoff`
  - `triggered = true` なら、active frontier の source docs sync や block close 裁定を優先する narrow 返送が runtime で発火している
  - ticket / chunk の close-ready は `task_planner`、block close-ready は `plan_manager` が返り得る
  - skill 本文側ではこれを再解釈せず、runtime の `next_role` をそのまま読む
- `reviewer_pass_through`
  - `triggered = true` かつ `blocking = false` なら、code ticket 後段の internal role として `reviewer` を先に通す
  - `blocking = true` なら reviewer finding が未解消なので、その turn を止めて人間へ返す
  - reviewer pass-through は direct target の追加ではなく、bounded run 内の内部処理としてだけ扱う
- `stop_reason`
  - hard stop のときだけ downstream を止める
  - `next_role` と `evidence` をそのまま人間へ返す
- `dispatchable`
  - `false` ならその turn では downstream を起動しない
- `bounded_multi_step`
  - `MID` は「1 block を終わらせる側の既定 level」として読む
  - active block だけが残り、次に必要なのが chunk / ticket 生成なら、`MID` でも `task_planner` への 1 段 handoff を許す
  - step 上限は `max_steps_per_run` を runtime 出力から読む
  - `HIGH` はその `MID` を含んだまま、より広い bounded run を許す上位 level として読む
  - `execution_level` と `max_steps_per_run` を対で読み、`HIGH` でも full auto や hard stop 無効化はしない
  - step ごとに `flow_conductor.py` を再実行し、skill 本文側で route を推測し続けない
- `advisories`, `promotion_candidates`, `sync_warnings`
  - downstream role に渡す補助情報として扱う
  - これだけを理由に `route_hint` を上書きしない
  - close-ready handoff は advisory ではなく runtime 自体の narrow route 変更として扱う

## downstream 実行ルール
- `plan-manager`
  - block の裁定、plan 更新、上流判断が必要なときの返送先
- `task-planner`
  - ticket / chunk / handoff / 昇格同期が必要なときに起動する
- `task-worker`
  - active ticket の実行が可能なときに起動する
- `reviewer`
  - code ticket の後段で `task-worker` が handoff する
  - human-facing direct target には増やさないが、`reviewer_pass_through.triggered = true` のときだけ bounded run の internal role として起動してよい

## 運用上の注意
- package では runtime asset は `tools/conductor/` 配下を正とする
  - `tools/conductor/flow_conductor.py`
  - `tools/conductor/run_conductor.sh`
  - `tools/conductor/add_operator_request.sh`
- `.agents/skills/` が存在しても export mirror として扱い、canonical source は `tools/codex-skills/` のまま読む
- package の first-pass でも same-block bounded auto に限り、既定は `MID / 5 step` で進めてよい
- practical override が必要なら `LEVEL=HIGH step=20` のような明示指定を使い、無制限化はしない
- `MID` では 1 block を終わらせる側の既定として読み、block-only 状態なら chunk / ticket 生成だけを `task_planner` へ渡す narrow handoff を含めてよい
- block close-ready 段階では execution level に関わらず `plan_manager` 返送を優先する
- `reviewer` pass-through、docs-only skip、hard stop の境界は既存 role skill の contract に従う
