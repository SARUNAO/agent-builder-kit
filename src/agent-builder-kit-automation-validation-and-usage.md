# 検証と使い方

このチャプターで最初に知ってほしいのは、「いま自分がどう使えばよいか」です。  
検証結果はその裏付けとして扱い、まずは daily use の形から説明します。

## まず覚える使い方

日常運用では、入口は `conductor` だけに寄せられます。  
人間が覚える形は次の 2 つで十分です。

```text
[$conductor] LEVEL=MID step=5
[$conductor] LEVEL=HIGH step=20
```

読み方はシンプルです。

- `MID / 5`
  - 1 block を終わらせる側の既定
- `HIGH / 20`
  - より強めに進めたいときの上位設定
  - ただし無制限 auto ではない

迷ったらまずは `MID / 5` で始めます。  
block をかなり先まで進めたいときだけ `HIGH / 20` を使えば十分です。

## hard stop は失敗表示ではなく安全装置

ここで重要なのは、hard stop を「壊れた表示」と読まないことです。  
hard stop は、そこで人間へ返すべきだと分かった境界を示しています。

代表例は次の 3 系統です。

- pending operator request
- loop retry detected
- bundled confirmations detected

これらが出たときは、自動続行より人間判断を優先します。  
むしろ hard stop が見えることで、「どこまで自動で進め、どこで止めるか」が読みやすくなります。

## キューは「あとで拾う要求置き場」として使う

途中で追加したい要望が出たら、キューへ積みます。  
ここでの考え方は「今すぐ割り込ませる」ではなく、「次の安全境界で確実に拾う」です。

たとえば次のように request を追加します。

```bash
bash scripts/add_operator_request.sh --summary "追加したい要望"
```

流れは次のとおりです。

1. 人間が request をキューへ積む
2. current ticket が終わる
3. `conductor` が pending request を検知する
4. hard stop として upstream role へ返す

この読み方を守ると、「後から一言差し込みたい」が unsafe な途中割り込みになりません。

## Codex Action を使うとワンボタン化できる

毎回手でコマンドを書くのが面倒なら、Codex アプリの Action を使います。

手順は次のとおりです。

1. `設定`
2. `環境`
3. プロジェクト名横の `+`
4. `アクションを追加`
5. `bash` を登録

たとえば `bash scripts/run_conductor.sh --human` を Action にしておけば、UI 上部タブからワンボタンで `conductor` 入口を呼べます。

ここで大事なのは、Action は main contract ではなく人間向けの近道だということです。  
正本はあくまで `conductor` skill と `run_conductor.sh` です。

## 実際の検証で何を見たか

この段階で見たかったのは、未来の完全自動化ではありませんでした。  
まず確認したかったのは、「docs 駆動の flow を壊さずに `conductor` を差し込めるか」です。

観点は大きく 5 つでした。

- 通常実行で current state と next role が自然に読めるか
- pending operator request があるときに、安全境界でちゃんと差し戻せるか
- 段階実行（bounded multi-step）で `task_worker`、`task_planner`、`plan_manager` の返送境界が読めるか
- reviewer pass-through を no-findings path では通し、blocking finding では止められるか
- status 同期漏れのようなズレを warning として拾えるか

つまり「便利そうか」ではなく、「実際の flow の中で役割を持てるか」を見ました。

## 通常実行で分かったこと

通常実行では、`run_conductor.sh --human` で summary が読め、JSON 正本も壊れず返ることを確かめました。
ここで価値があったのは、派手な自動化より「いま何が起きているか」が読みやすくなることでした。

`next_role`、pending request 数、完了候補、同期警告がまとまって見えるだけでも、人間が頭の中で role の流れをつなぎ直す負荷はかなり下がります。

## pending request で分かったこと

queue を使った差し込み要求も、想定どおり機能しました。

- request を追加する
- current ticket が終わる
- `conductor` が pending request を検知する
- `task_planner` へ返る

この流れが確認できたことで、queue は単なる補助 script ではなく、運用上の安全装置として成立していると分かりました。

## 段階実行で分かったこと

段階実行を入れたあとに確認したかったのは、same-turn で本当に handoff が見えるかでした。
そこで close-ready handoff を足したあと、`task_worker -> task_planner -> task_worker` の visible handoff が current repo で観測できるようになりました。

つまり bounded multi-step は「何となく先へ進む」ではなく、

- どこまで同じ turn で進むか
- どの境界で返るか

が読める形へ進んだわけです。

## `MID/HIGH` と `step` の override で分かったこと

override を入れたあとに確認したのは次の 3 点です。

- default は `MID / 5`
- `HIGH / 20` で bounded override が有効になる
- それでも hard stop は override より優先される

ここで重要なのは、`HIGH / 20` を入れても unlimited 実行にはならないことです。  
hard stop、reviewer blocking、`plan_manager` 境界、step 上限があれば必ず止まります。

## reviewer pass-through で分かったこと

reviewer pass-through は、no-findings path と blocking path で挙動がはっきり分かれました。

- no-findings path
  - `task-worker -> reviewer -> task-planner`
- blocking finding
  - reviewer 境界で止まる

この差が見えたことで、「reviewer を毎回人間入口の direct target にしなくても、必要なところだけ bounded run 内へ通せる」と確認できました。

## warning で分かったこと

status 同期漏れや table / frontmatter mismatch のような warning も temp copy で検証しました。
ここで分かったのは 2 つです。

- warning の検知自体は効く
- ただし warning だけで route が強く切り替わるわけではない

つまり `conductor` は warning を見えるようにはするが、そこで何でも裁定する主体ではまだありません。  
この限界も、実際の観測結果として確認できました。

## いまの使い方を一言でまとめると

現時点の `conductor` は、無制限 auto の agent ではありません。  
docs を読み、段階的に flow を整え、人間へ「次に何をすればよいか」を見せる入口です。

使い方としては次で十分です。

- まず `[$conductor] LEVEL=MID step=5`
- 強めに進めたいときだけ `LEVEL=HIGH step=20`
- 後から要望を足したいときはキューを使う
- hard stop が出たら「ここで人間へ返す境界だ」と読む

次の中チャプターでは、ここまでで何が実用になり、何を residual として残したかを短く整理します。
