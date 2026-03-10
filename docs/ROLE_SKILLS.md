# Role Skills

この docs は、運用 role を skill として実行するときの連携ルールを定義する。

## 目的
- role ごとの思考範囲を狭める
- docs 更新順と更新権限を固定する
- role skill の終端で `.canvas` を自動同期する

## skill 一覧
- `plan-manager`
- `task-planner`
- `task-worker`
- `reviewer`
- `obsidian-canvas-sync`
- `docs-sync`（planned, not shipped）

## canonical 名
- canonical 名:
  - `plan-manager`
  - `task-planner`
  - `task-worker`
  - `reviewer`
- 利用者向け docs、README、package docs では canonical 名だけを案内する

## 実行モデル
- role skill は source docs を更新する主担当
- `obsidian-canvas-sync` は末尾の同期担当
- role skill が更新を終えたら、同ターンの最後に canvas sync を呼ぶ

## skill asset の置き場
- canonical source:
  - `tools/codex-skills/`
- user-facing export 層:
  - `.agents/skills/`
- ルール:
  - source repo と `agent-builder-kit` では `tools/codex-skills/` を正本として扱う
  - `agent-builder-kit` 自体には `.agents/skills/` mirror を必須としない
  - generated repo で `.agents/skills/` が存在する場合、利用者はそちらを入口として読んでよい
  - ただし `.agents/skills/` は export mirror であり、source of truth ではない
  - `.agents/skills/` が未生成の profile / phase では `tools/codex-skills/` を読む

## `docs-sync` support skill の位置づけ
- `docs-sync` は、role skill が意味判断を終えたあとの docs 整合だけを扱う補助 skill とする
- 想定責務:
  - `docs/references/*.md` の summary view を本体 docs に追従させる
  - `docs/exec-plans/active/attention-queue.md` と `docs/references/attention-queue.md` の summary 整合を取る
  - 必要なら `docs/PLANS.md` や hub docs の軽微な整合を取る
- やらないこと:
  - block / chunk / ticket の意味変更
  - 人間要求の再解釈
  - 実装コードの変更
- 現時点では contract のみ定義し、generic package にはまだ同梱しない
- 実装する場合は `obsidian_canvas pack` の一部として ship し、canvas / reference band を使わない profile へは載せない

## reference band との責務分界
- reference band の直接正本は `docs/references/*.md`
- ただし reference note の意味上の本体 docs は別にある
  - `Product Sense` -> `docs/PRODUCT_SENSE.md`
  - `Design` -> `docs/DESIGN.md`
  - `Attention Queue` -> `docs/exec-plans/active/attention-queue.md`
  - `Human Manual` -> `docs/HUMAN_MANUAL.md`
- role skill はまず本体 docs を更新し、その変更が reference band に見えるべき場合だけ対応する `docs/references/*.md` を追従させる
- reference note を本体 docs の代替正本として更新してはならない
- `docs-sync` を導入する場合も、この責務分界は維持する
- つまり role skill が本体 docs を更新し、`docs-sync` は summary / hub の追従だけを行う

## orchestration rule

### `plan-manager`
1. `docs/exec-plans/project-intake.md`, `docs/exec-plans/discovery-brief.md`, `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks/*.md` を読む
2. 上流判断を更新する
3. 各 block に実際に着手する直前に、人間へ仕様の聞き取りを行う
4. 聞き取りでは必要に応じて、言語、開発フレームワーク、設定方針、依存、テスト方針を明示的に詰める
5. 聞き取りと同時に、現時点で妥当なおすすめ案を 1 つ以上提示し、採用理由と主要な trade-off を残す
6. block の追加、削除、改名、差し込み順、`Done チェック` を反映する
7. 新しい block を追加したら、どこに差し込むかと既存順序が妥当かを必ず再判定する
8. chunk / block を `done` に上げる前に source docs sync を確認する
9. 必要な `done` 昇格を反映する
10. block 順序または status が変わったら `obsidian-canvas-sync` を実行する
11. `docs/PRODUCT_SENSE.md`, `docs/DESIGN.md`, `docs/HUMAN_MANUAL.md` を変えた場合は、対応する `docs/references/*.md` の summary 追従要否も判断する
12. `task-planner` が roll-up 整合のため親 block を `pending -> in_progress` へ同期した場合は、その状態を正として扱い、以後の `done` / `blocked` 判断を引き続き担当する

## `plan-manager` の聞き取りルール
- block の実装着手前に、未確定の仕様を人間へ確認する
- 典型的な確認項目:
  - 実装言語
  - 開発フレームワーク
  - 設定方針
  - データ保存や外部連携の前提
  - テスト / lint / review の期待値
- ただ質問するだけでなく、`plan-manager` 自身が推奨案を出す
- 推奨案には、採用理由と主要な代替案との差分を短く添える
- block が docs 主体でも、実装判断が後続で必要になるなら先に確認を取る
- すでに block note や discovery に十分な確定情報があるなら、重複質問は避けてよい

### `task-planner`
1. `docs/exec-plans/plan-spec.md` と `docs/exec-plans/blocks/*.md` を読む
2. `docs/exec-plans/chunks/*.md`, `docs/exec-plans/tickets/*.md` を更新する
3. chunk / ticket の親子関係、順序、`Done チェック` を反映する
4. ticket を `done` に上げる前に ticket / fact-report / chunk table の同期を確認する
5. ticket 完了ごとに、追加の chunk / ticket / block が必要かを必ず再判定する
6. 必要な ticket `done` 昇格と chunk handoff を反映する
7. 配下 chunk を `in_progress` または `done` に上げた結果、親 block が roll-up 上 `in_progress` になるのに `pending` のままなら、親 block の `pending -> in_progress` も同期してよい
8. この例外は整合同期に限り、block の goal / depends_on / 順序変更や `done` / `blocked` 判断は行わない
9. `obsidian-canvas-sync` を実行する
10. `docs/exec-plans/active/attention-queue.md` を更新した場合は、`docs/references/attention-queue.md` の追従要否も判断する

### `task-worker`
1. 対象 ticket と関連 chunk を読む
2. 実装を行い、ticket の事実と `fact-report` を更新する
3. コード編集がある ticket では、実装後に `reviewer` へ handoff する
4. markdown / docs 主体でコード編集がない ticket では、reviewer 呼び出しを skip してよい
5. skip する場合は、ticket または `fact-report` に docs-only skip であることを残す
6. 依存関係の変化で単体完了できない場合は `blocked` を使い、理由を ticket と fact-report に残す
7. 必要なら chunk close へ戻す材料を残す
8. `obsidian-canvas-sync` を実行する

### `reviewer`
1. `task-worker` が終えた code ticket を読む
2. コード、命名規則、フォールバック、境界逸脱、テスト不足を確認する
3. findings を先に出し、ticket の `Done チェック` に reviewer 観点の sign-off を反映する
4. docs-only skip になっている ticket では介入しない
5. chunk / block の ownership は変えない

## reviewer handoff rule
- 原則:
  - コード編集がある ticket は `task-worker` のあとに `reviewer` を呼ぶ
- skip を許す条件:
  - markdown / docs 更新のみ
  - 設定値や文言の変更で、コードパスや命名、フォールバックを増やしていない
- 曖昧な場合:
  - skip せず reviewer を優先する
- current state:
  - source repo / `agent-builder-kit` / generated repo の 3 面に reviewer asset を載せる
  - generated repo では `task-worker` 後段の reviewer handoff docs を読む

## reviewer sign-off
- ticket の `Done チェック` には reviewer 観点の承認を含める
- ただし reviewer 承認だけで `status = done` にはしない
- `task-planner` が docs sync と整合を確認して昇格させる
- docs-only skip の場合は、その理由を ticket か `fact-report` に明記したうえで `task-planner` へ渡す

## canvas sync の呼び方
- role skill は `obsidian_canvas_pack` が有効なときだけ sync を実行する
- 実行前に、必要な source docs が揃っているか確認する
- source docs の更新がなければ再同期を省略してよい

```bash
python3 tools/codex-skills/obsidian-canvas-sync/scripts/sync_canvas.py \
  --plan-spec docs/exec-plans/plan-spec.md \
  --block-dir docs/exec-plans/blocks \
  --chunk-dir docs/exec-plans/chunks \
  --ticket-dir docs/exec-plans/tickets \
  --reference-dir docs/references \
  --vault-root path/to/vault-root \
  --canvas docs/exec-plans/canvas/development-flow.canvas
```

## 失敗時の扱い
- role skill は source docs 更新を優先する
- `.canvas` sync が失敗した場合、docs を正本として残し、失敗内容だけを報告する
- `.canvas` を手で直して source docs の代わりにしない

## まだ分けないもの
- `plan-manager` と `仕様設計者` の分離 skill

reviewer 分離は contract 定義、asset 実装、bootstrap 反映まで閉じた。

## 移行中の注意
- role skill の正本は `docs/exec-plans/` と `docs/references/` を使う
- legacy layout を読む必要がある場合は、manifest override を前提に明示的に扱う
- `docs/references/*.md` は canvas 用の summary view であり、本体 docs を置き換えない
- reference band の自動同期責務は、`TICKET-017` の判断により support skill `docs-sync` へ分離してよいものとして扱う

## `TICKET-017` 時点の決定
- `docs-sync` は support skill として分離してよい
- ただし generic package の共通骨格には含めず、将来実装する場合のみ `obsidian_canvas pack` の add-on asset として扱う
- それまでの暫定運用では、role skill が reference / hub 更新を同ターンで担う

## `TICKET-025` 時点の決定
- `task-worker` とは別に code review 専用 canonical 名 `reviewer` を定義する
- generated repo と package には `reviewer` だけを配り、旧 alias は同梱しない
- コード編集あり ticket では `task-worker` 後段で reviewer を呼ぶ
- markdown / docs 主体 ticket は docs-only skip を明示したうえで reviewer を省略できる

## `TICKET-028` 時点の決定
- `tools/codex-skills/` を canonical source として維持する
- `.agents/skills/` は利用者向け export 層として定義する
- generated repo で `.agents/skills/` が存在する場合は入口をそちらへ寄せてよい
- ただし source repo / package docs / bootstrap contract の正本は引き続き `tools/codex-skills/` に置く
