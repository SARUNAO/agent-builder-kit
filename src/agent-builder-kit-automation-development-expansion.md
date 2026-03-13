# bounded multi-step 以後の拡張

ここから先で扱うのは、「`conductor` が実際にどこまで進められる入口になったか」です。  
読者として先に見てほしいのは、内部実装の列挙ではなく、次の 4 点です。

- どこまで自動で進み、どこで止まるのか
- `LEVEL=MID` と `LEVEL=HIGH` をどう使い分けるのか
- reviewer をどこまで same-turn で通せるのか
- package 側へ何を戻し、何を戻さなかったのか

## まず広げたのは「段階実行」だった

`conductor-only` entry が成立したあと、次に必要になったのは「人間が毎回 `task-worker` と `task-planner` を呼び直さなくても、同じ block の中ではある程度先へ進めたい」という要求でした。

ここで採ったのは、無制限 auto ではなく、段階実行（bounded multi-step）です。

最初に固めた contract は次のとおりでした。

- 既定は `LEVEL=MID`
- `MID` では同一 active block の中を進める
- 既定の上限は `5` step
- hard stop、`plan_manager` 境界、reviewer blocking、step 上限で止まる

重要なのは、「進める」ことより「どこで止まるか」を先に固定した点です。
この順序を守ったことで、bounded multi-step を足しても既存 role の裁定権は壊れませんでした。

## close-ready handoff を足して、見える挙動にした

段階実行を入れた直後は、docs 上では正しくても、人間から見ると `task-worker` 側に張り付いて見える gap が残りました。
そこで追加したのが close-ready handoff です。

ここでやったのは、`promotion_candidates` 全体を強い route 変更理由にすることではありません。  
active frontier 自体が close-ready で、`task-planner` に source docs sync をさせないと次へ進めないときだけ、same-turn で `task_planner` に返す narrow policy を足しました。

この修正で、`task_worker -> task_planner -> task_worker` の visible handoff が成立しました。
人間から見ても「段階実行が本当に same-turn でつながっている」と分かるようになったのが、この段階の大きい改善です。

## `LEVEL=MID|HIGH step=<num>` はどう使うか

次に出た要求は、「5 step 固定だと block の規模によって短い」というものでした。
ただし、ここでも上限撤廃はしませんでした。

整理した run level は次のとおりです。

- `LEVEL=MID`
  - 1 block を終わらせる側の既定
  - active block しか無く、次に必要なのが chunk / ticket 生成なら `task_planner` への 1 段返送も含む
- `LEVEL=HIGH`
  - その `MID` を含んだまま、block close-ready では `plan_manager` 返送を優先する上位 level
- `step=<num>`
  - 既定 `5` を上書きする bounded override

たとえば日常運用なら次の 2 つを覚えておけば十分です。

```text
[$conductor] LEVEL=MID step=5
[$conductor] LEVEL=HIGH step=20
```

ここでの `step=20` は「無制限にする」ではなく、「今回の block は実質最後まで進めたいので cap を大きめにする」という意味です。

## `HIGH` でも何でも自動で進むわけではない

`HIGH` を入れると、block 間を何でも進めてよいと誤解しやすくなります。
実際にはそうしていません。

`HIGH` の cross-block handoff は、child chunk 未生成の block-only 状態に限定しました。
既に child chunk がある block-only 状態では、上流裁定が残っている可能性が高いので `plan_manager` を優先します。

つまり `HIGH` は「強い自動化」ではなく、

- 1 block をかなり先まで進める
- そのうえで block close-ready では `plan_manager` 返送までを受ける

という bounded な上位設定です。

## 人間向け override は準正規形に寄せた

ここは使い勝手に直結する部分でした。
自然文の完全自由入力より、`LEVEL=MID|HIGH step=<num>` の準正規形を強く求める方が安全です。

そのため human 側にも、たとえば次のような形を使う前提に寄せました。

```text
[$conductor] LEVEL=HIGH step=20
```

skill 側はこれを `--level` と `--max-steps` に正規化して runtime へ渡します。
この折衷のおかげで、使い方はシンプルに保ちつつ、解釈の揺れを減らせました。

## reviewer は no-findings path だけ same-turn で通した

code ticket のたびに reviewer 境界で必ず止まると、段階実行の価値が薄くなります。
一方で、重大 finding を素通りさせるわけにはいきません。

そこで reviewer pass-through は 2 段で整理しました。

- no-findings path では `task-worker -> reviewer -> task-planner`
- blocking findings があるときだけ return boundary

この形にしたことで、reviewer を人間入口の direct target に増やさず、それでも same-turn bounded run を無駄に止めずに済むようになりました。

## package backport では current repo 固有ログを持ち込まなかった

current repo で bounded multi-step、`MID/HIGH`、reviewer pass-through が固まったあと、generic な差分だけを package へ戻しました。
ここで重要だったのは、current repo 固有の validation 実測や temp fixture 名、fact-report をそのまま package へ混ぜないことでした。

戻したのは主に次の帯です。

- runtime
- skill
- shared contract docs

逆に current repo 固有の観測は local validation として残し、package には generic contract だけを戻しました。
この切り分けをしないと、後から package を読む人にとって「何が一般化された仕様で、何がこの repo 固有の記録か」が分かりにくくなります。

## この段階でまだ見送ったもの

ここで大事なのは、実装したものだけではありません。  
何をまだ決めないまま残したかも同じくらい重要です。

たとえば、

- warning 時に route をどこまで変えるか
- `.canvas` sync を将来的にどこへ集約するか
- package bootstrap 前の default path をどう整えるか

といった論点は、この段階では「解決済みの設計」としては書かないことにしました。
最小実装として確認できた事実を越えるからです。

## ここまでで自分が読むべきポイント

このチャプターを読み終えたら、少なくとも次の理解が残れば十分です。

- `conductor` は bounded に数 step 進める入口になった
- 既定は `MID / 5`
- `HIGH / 20` は強めだが bounded な上位設定
- reviewer は no-findings path だけ same-turn で通す
- package へは generic contract だけを戻す

次のチャプターでは、これを実際に使うときに何が便利で、どこで hard stop やキューを使うかを扱います。
