# plan-manager でプロジェクトの骨子を組む

`agent-builder-kit` を展開したら、次にやることは実装ではありません。まず `plan-manager` を使って、このプロジェクトで何を作るか、どこまでを初回ゴールにするか、その骨子を組みます。

`plan-manager` は、要求整理と上流の計画更新を担当する role です。人間から受け取った要望をそのまま流すのではなく、確認済み事実、仮置き前提、未確定事項を分けながら、後続の role が迷わない骨組みへ整えます。

この段階で主に更新されるのは、次の docs です。

- `docs/exec-plans/project-intake.md`
- `docs/exec-plans/discovery-brief.md`
- `docs/exec-plans/plan-spec.md`
- `docs/exec-plans/blocks/*.md`

使い方はシンプルで、「何を作りたいか」と「いま分かっていること」を `plan-manager` に渡します。すると `plan-manager` は、block 単位の実行計画へ落とし込み、必要なら「何を先に決めるべきか」も返します。

たとえば今回の project では、mdBook を作ること自体よりも、`agent-builder-kit` を使った docs 駆動フローをどうワークショップ化するかが主題でした。そのため `plan-manager` は、公開ゴール、章構成、記録基盤、公開導線といった論点を block に分けて整理するところから始めています。

大事なのは、ここで細かい実装へ飛ばないことです。まず骨子を作ってから、次の `task-planner` が chunk と ticket へ分解する流れに入ることで、あとから見返しても追いやすい開発フローになります。


では実際に、私がこのmdbookを作るにあたって最初に発した言葉を見返してみます。
```
$Plan Manager  環境を構築したところで、今は何もつくっていません
```

Skill化した``

次の章では、その骨子がどのように chunk と ticket へ分解され、role ごとの handoff につながるのかを見ていきます。
