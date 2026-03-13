# agent-builder-kit で開発を進める

このチャプターでは、`agent-builder-kit` を使った docs 駆動開発が、実際にはどの順で進んでいくのかをまとめます。
ここで扱うのは個別の機能追加ではなく、`plan-manager` から `task-worker`、そして本文化までをどうつないでいくかという全体の流れです。

## このチャプターの読み方

最初に [plan-manager で骨子を組む](./plan-manager-skeleton.md) を読むと、project の要求をどう block に整理するかが見えてきます。

次に、

- [task-planner で仕事を chunk と ticket に分ける](./task-planner-breakdown.md)
- [task-worker で ticket を実行し、fact-report を返す](./task-worker-execution.md)
- [開発ログからチュートリアル本文を組み立てる](./process-to-article.md)

の順に追うと、計画の分解、実装、記録の再編集までを一続きの流れとして追えます。

最後の [ハーネスエンジニアリングをさらに進める](./true-harness-engineering.md) では、ここまでの流れを土台に、さらに先の設計観点を考えます。

## このチャプターで扱うこと

このまとまりでは、主に次の論点を扱います。

- 要求整理を、どう block / chunk / ticket へ落としていくか
- role ごとに、どこまでを担当し、どこで次へ返すか
- `fact-report` や planning docs を、あとから本文へどう再構成するか
- `.canvas` を補助線としてどう見るか

つまりこのチャプターは、個別の作業内容そのものよりも、「開発フローをどのように運用すると破綻しにくいか」を読むための入口です。
