# なぜ conductor が必要だったのか

この project の出発点は、「`agent-builder-kit` はすでに使えるが、実際に回すと毎回細かい判断が残る」という感触でした。
plan を block、chunk、ticket に分けるところまでは整っていても、その先で人間が何度も「次は誰を呼ぶべきか」「追加要求をどこで差し込むべきか」「この結果を package や tutorial にどう戻すべきか」を考え直す場面が残っていたからです。

最初から目指していたのは、何でも自動化することではありませんでした。人間が裁定すべきところは残したまま、繰り返し出てくる role routing を薄く整えることが目的でした。そこから `conductor` を read-only advisor として足し、さらに bounded multi-step、`LEVEL=MID|HIGH step=<num>`、reviewer pass-through へ広げていったのが今回の流れです。

## なぜ追加の自動化が必要だったのか

`agent-builder-kit` の基本的な流れは、すでにかなり整理されています。
`plan-manager` が骨子を作り、`task-planner` が chunk と ticket に分解し、`task-worker` と `reviewer` が実行と確認を進める、という流れです。

ただ、実際にしばらく運用すると、次のような摩擦が見えてきます。

- 複数の ticket をまたぐと、次にどの role を呼ぶか毎回人間が思い出す必要がある
- shell や bash loop で半自動化しようとすると、人間の差し込み要求をどこで拾うかが曖昧になる
- 開発ログを public な tutorial へ流したいが、internal な planning docs と公開記事の境界を保つ必要がある

ここで見えていたのは、役割の不足ではなく、役割同士のあいだを読む薄い制御層の不足です。
すでに `plan-manager` も `task-planner` も `task-worker` もいるのに、role の切り替えや差し込み要求の扱いでは毎回人間が流れをつなぎ直していました。

つまり足りないのは、実装能力ではなく「流れを読む薄い制御層」でした。
この project では、その制御層を `conductor` として設計しています。

## この project は何をやっているのか

実際には、この project は 1 つの機能追加だけをやっていたわけではありません。
途中で要求が足されるたびに、次の 3 本を並行して整理する必要が出ました。

- `conductor` という read-only な制御層を追加する
- queue を使って loop 実行中の人間要求を安全境界で差し込めるようにする
- `conductor-only` entry から same-block bounded multi-step、さらに `HIGH` の narrow cross-block handoff まで広げる
- reviewer pass-through と package backport を既存 role 契約の上で追加する
- 開発中の判断や結果を mdBook 側へ流せるよう、記録と公開の導線を整える

ここでいう `conductor` は、計画そのものを書き換える役ではありません。
むしろ最初に決めたのは、「何でもできる orchestration agent にしない」ことでした。
`plan-manager`, `task-planner`, `task-worker`, `reviewer` の既存の役割分担を壊さずに、現在の docs を読んで「次は誰が動くべきか」を案内する役として置いています。

## `conductor` は何をするのか

初期版の `conductor` は、docs を正本として読んだうえで、次にどの role へ戻すべきかを返すだけの軽い役割に留めます。その後、設計を壊さない範囲で bounded multi-step の入口へ広げましたが、今でも status 意味変更や最終裁定までは持ちません。

やることは主に次の 3 つです。

- `plan-spec`, `blocks`, `chunks`, `tickets`, `operator requests` を読み、現在の状態を集約する
- pending の operator request があるかを確認する
- 次に `task-planner` へ戻すべきか、通常どおり次 ticket を進められるかを案内する
- `LEVEL=MID` では同一 block 内だけ、`LEVEL=HIGH` では block-only 状態から narrow handoff を許す
- bounded run の中で `task-worker -> reviewer -> task-planner` の pass-through を通す

加えて、`promotion_candidates` や `sync_warnings` を返して、機械的に見つけられる同期漏れを可視化します。
ただし、ここで大事なのは `conductor` が read-only だという点です。
status の更新や最終裁定は引き続き `task-planner` / `plan-manager` が持ちます。

この境界は途中で何度も再確認されました。
warning が出たときにもっと強く差し戻した方がよいのではないか、`.canvas` sync まで `conductor` に集約した方が自然ではないか、という話も出ましたが、この段階では「まずは read-only でどこまで役に立つかを見る」方針に留めています。

## 人間要求をどこで差し込むのか

今回の拡張で強く効いた要求の 1 つが、「bash で loop を回している最中に、今の ticket が終わったら一言差し込みたい」というものでした。
これは単なる UI の話ではなく、安全境界をどこに置くかという設計の話でもあります。

この project では、実行中の ticket を無理に止めるのではなく、安全境界を `after_current_ticket` に固定します。
つまり、今の ticket が終わったあとにだけ pending request を拾い、次の流れを再判定する形です。

そのために、`docs/exec-plans/operator-requests/REQ-*.md` という request file を追加していきます。人間は template から request を作るだけでよく、`conductor` はそれを読んで「まず `task-planner` へ返す」「必要なら `plan-manager` へ上げる」と案内する設計です。

この方式の利点は、すべてを docs 正本の世界に留められることです。
メモリ上の一時イベントではなく、あとから見返せる記録として残るため、開発ログとしても扱いやすくなります。

## current repo と tutorial repo の役割分担

この project では repo を 2 つに分けていますが、同じ内容を二重管理したいわけではありません。
むしろ、途中で「何を generic package に戻し、何をこの repo 固有に残すか」を整理した結果、この分担がはっきりしました。

役割は次のように分かれます。

- current repo
  - 進行中の計画、ticket、fact-report、設計メモを保持する
  - まだ公開向けに整っていない試行錯誤も残す
  - `conductor`、operator request、run level、reviewer pass-through のような運用設計の正本を持つ
- package repo (`agent-builder-kit`)
  - generic runtime、shared role-skill 契約、最小限の docs を受ける upstream として扱う
  - current repo 固有の validation 実測や temp fixture 名は持ち込まない
- tutorial repo
  - current repo で残した記録を、読者向けの説明順に並べ替えて公開する
  - 内部運用の細かい文脈をそのまま出すのではなく、理解に必要な部分だけを抜き出す
  - mdBook として読みやすい章構成を保つ

つまり、current repo は開発現場の正本であり、tutorial repo は説明用の再編集物です。
この線引きを先に決めておくことで、「とりあえず両方に同じことを書く」という非効率を避けやすくなります。

## このあと何を読むか

ここから先は、前段のガイドを踏まえたうえで次の流れで読むのが自然です。

- `開発のメインパート`
  - `conductor-only` entry、bounded multi-step、`MID/HIGH`、reviewer pass-through、package backport の中核部分
- `検証・使い方・統括`
  - hard stop、queue、Codex Action、`[$conductor] LEVEL=MID|HIGH step=<num>`、代表シナリオの観測結果、締めの整理

この章は、読者が「この拡張は何のためにあり、どの要求追加が設計変更を呼び、どこまでを最小実装として扱ったのか」を先に掴むための入口です。
