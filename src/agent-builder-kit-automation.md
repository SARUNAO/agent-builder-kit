# conductor を加えて開発フローを自動化する

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

まずは [なぜ conductor が必要だったのか](./agent-builder-kit-automation-overview.md) で、「なぜ `conductor` を足したのか」「current repo と package と tutorial repo をどう役割分担したのか」を掴むのが早道です。

そのうえで、次の順に読むと自然につながります。

- [read-only な conductor から始める](./agent-builder-kit-automation-development.md)
- [bounded multi-step と run level を加える](./agent-builder-kit-automation-development-expansion.md)
- [conductor の使い方と検証結果](./agent-builder-kit-automation-validation-and-usage.md)
- [conductor 拡張の到達点](./agent-builder-kit-automation-summary.md)

前半ほど「なぜ必要だったか」、後半ほど「どう使い、何が確認できたか」に寄ります。

## この章全体で持ち帰ってほしいこと

この章全体で見てほしいのは、細かな実装一覧ではなく次の流れです。

- なぜ `agent-builder-kit` に追加の自動化が必要だったのか
- `conductor` を read-only advisor から段階実行の入口へどう広げたのか
- それを日常運用でどう使い、どこに安全境界を置いたのか

親章であるこのページは、各中チャプターをつなぐハブです。  
どこから読めばよいか迷ったら、このページへ戻ると全体の流れを追い直せます。
