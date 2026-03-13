# agent-builder-kitを拡張して自動化する

この章で扱うのは、「新しい agent を 1 つ足した」という話ではありません。  
人間が毎回 role を選び直さなくても進められる入口をどう作るか、そしてその入口をどこまで安全に広げるか、という話です。

もともと `agent-builder-kit` には block、chunk、ticket を回す土台がありました。  
ただ実運用では、次のような細かな判断が残ります。

- 次にどの role を呼ぶか
- 人間の差し込み要求をどこで拾うか
- reviewer をどこまで same-turn で通すか
- 公開用の mdBook 本文へどこまで引き上げるか

そこで current repo では、薄い制御層として `conductor` を足しつつ、

- 段階実行（bounded multi-step）
- `LEVEL=MID|HIGH step=<num>`
- reviewer pass-through
- package backport

までを段階的に固めました。この章は、その流れを「まずどう使うか」が見える形で読み直すための入口です。

## この章の読み方

まずは [背景と全体像](./agent-builder-kit-automation-overview.md) で、「なぜ `conductor` を足したのか」「current repo と package と tutorial repo をどう役割分担したのか」を掴むのが早道です。

そのうえで、次の順に読むと自然につながります。

- [read-only 期と入口づくり](./agent-builder-kit-automation-development.md)
- [bounded multi-step 以後の拡張](./agent-builder-kit-automation-development-expansion.md)
- [検証と使い方](./agent-builder-kit-automation-validation-and-usage.md)
- [ここまでの統括](./agent-builder-kit-automation-summary.md)

前半ほど「なぜ必要だったか」、後半ほど「どう使い、何が確認できたか」に寄ります。

## 各中チャプターで何を読むか

- `read-only 期と入口づくり`
  - `conductor` をどこまで read-only に留めるか
  - operator request や warning をどう安全に扱ったか
- `bounded multi-step 以後の拡張`
  - 段階実行、`MID/HIGH`、reviewer pass-through、package backport をどう足したか
- `検証と使い方`
  - hard stop、キュー、Codex Action、`[$conductor] LEVEL=MID|HIGH step=<num>` の使い方
- `ここまでの統括`
  - 何が実用になり、何を後続論点として残したか

## この章全体で持ち帰ってほしいこと

この章全体で見てほしいのは次の点です。

- なぜ `agent-builder-kit` に追加の自動化が必要だったのか
- `conductor` を read-only advisor から段階実行の入口へどう広げたのか
- `LEVEL=MID` と `LEVEL=HIGH`、`step=<num>` をどう使い分けるのか
- hard stop とキューをどう人間向けの安全装置として扱うのか
- reviewer pass-through と package backport をどう既存 role 契約の上で追加したのか

親章であるこのページは、各中チャプターをつなぐハブです。  
どこから読めばよいか迷ったら、このページへ戻ると全体の流れを追い直せます。
