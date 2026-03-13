# read-only 期と入口づくり

このチャプターで先に掴んでほしいのは、「`conductor` に何をやらせないまま始めたか」です。  
自分でも `agent-builder-kit` を拡張したいなら、最初から強い自動化を目指すより、既存の role 契約を壊さない薄い入口を先に作る方が安全です。

ここでの要点は 3 つです。

- `conductor` は最初から何でも実行する agent にはしなかった
- 入口は 3 本の薄い script に分けた
- 後から差し込みたい要求は、途中割り込みではなくキューで扱うようにした

## 最初に決めたのは「全部やらせない」ことだった

今回の拡張で最初に大きかった判断は、`conductor` を何でもできる agent にしないことでした。
もしここで docs 更新や status 変更まで持たせると、`plan-manager`、`task-planner`、`task-worker` が持っていた責務境界が一気に曖昧になります。

そこで初期版では、`conductor` を read-only に留める方針を先に固めました。

- docs を読む
- current state を集約する
- 次に呼ぶ role を案内する

まずはここまでです。  
この判断が入ったことで、以後の実装は「何を足すか」より先に「これは既存 role の責務を奪わないか」で考えられるようになりました。

## 最小構成は 3 本の入口だった

最初に揃えたのは、厚い orchestration runtime ではなく、役割の違う 3 本の入口でした。

- `flow_conductor.py`
- `run_conductor.sh`
- `add_operator_request.sh`

それぞれの役割は明快です。

- `flow_conductor.py`
  - 状態を読み、次の role や hard stop を返す正本
- `run_conductor.sh`
  - 人間や Action から叩きやすいラッパー
- `add_operator_request.sh`
  - 後から差し込みたい要求をキューへ積む helper

この分け方の利点は、「どこが正本で、どこが人間向けの入口か」が崩れにくいことでした。
自分で拡張するときも、まずはこの 3 分割に近い構成から始めると、あとで責務が混線しにくくなります。

## 名前も設計の一部だった

この段階では rename も設計判断でした。
`flow-orchestrator` のような名前だと、何でも勝手に進める主体を連想しやすくなります。

そこで `conductor` という呼び名に寄せました。
意味としては「全部を実行する主体」ではなく、「今の状態を読んで次の動きを整える主体」に近いからです。

名前を変えるだけでなく、実際の役割もその名前に合わせました。
だからこの時点の `conductor` は、まだ「強い自動化」ではなく「薄い入口」です。

## 追加要求は途中割り込みではなくキューにした

運用を考えると、必ず出てくるのが「この ticket が終わったら、次にこれもやってほしい」という要求です。
ここで実行中 ticket の途中割り込みを既定にすると、一気に壊れやすくなります。

そこで、追加要求は `REQ-*.md` をキューとして積み、`after_current_ticket` の安全境界でだけ拾う形にしました。

流れは次のとおりです。

1. 人間が request file を作る
2. current ticket が終わる
3. `conductor` が pending request を検知する
4. hard stop として upstream role へ返す
5. `task-planner` が chunk / ticket 追加で閉じるかを判断する

この方式の良いところは、差し込み要求があとから見返せる docs になることです。
単なる割り込み制御ではなく、「何を追加したかったか」が記録として残ります。

## warning は「裁定」ではなく「見える化」に留めた

read-only 期で早く効いたのは、派手な自動化ではなく status 同期漏れの検知でした。
そこで `promotion_candidates`、`sync_warnings`、`table_frontmatter_mismatches` を返すようにしました。

ここでの狙いは、「機械的に見つけられるズレを見えるようにすること」です。

- 配下 ticket が終わっているのに chunk が `in_progress` のまま
- table と frontmatter がずれている
- close-ready だが source docs sync が残っている

ただし、直す主体は `conductor` ではありません。
実際に同期したり昇格したりするのは `task-planner` と `plan-manager` に残しました。

つまり `conductor` は、warning を見せることはできるが、そこで意味判断まで持つ主体ではないということです。

## 人間向け summary と JSON を分けた理由

`flow_conductor.py` の正本出力を JSON に置いたのは、script や Action から壊さず扱えるようにするためです。
一方で、人間が毎回 JSON を読むのはつらいので、`--human` では summary を出すようにしました。

この分け方のおかげで、

- 機械は JSON を読む
- 人間は summary を読む

という自然な役割分担ができます。

自分で似た仕組みを足すなら、「機械向け正本」と「人間向けの読みやすい出力」は最初から分けておく方が安全です。

## ラッパーを薄くしたのも理由がある

`run_conductor.sh` を厚くしすぎなかったのも、同じ考え方です。
ここで解釈ロジックまで抱え込むと、shell loop、Action、将来の別入口で挙動がずれやすくなります。

そのためラッパーの責務は、基本的に次の 2 つへ絞りました。

- `flow_conductor.py` を呼ぶ
- hard stop 時に人間向けの note と exit code を返す

この最小さがあったので、あとから `MID/HIGH` や close-ready handoff を足しても、core と入口を分けて考えやすいまま保てました。

## この段階で自分が真似するなら

もし自分でも `agent-builder-kit` を拡張するなら、この段階では次の指示から始めるのが自然です。

- `conductor` は read-only に留める
- docs 更新や status 変更は既存 role に残す
- 入口は Python 正本、ラッパー、追加要求 helper の 3 本に分ける
- 追加要求は途中割り込みではなくキューで扱う
- warning は見える化に留め、裁定は上流 role に残す

この段階で無理に「全部自動で進めたい」へ振らなかったことが、後段の拡張を安全にしました。

次のチャプターでは、この薄い入口を保ったまま、どこまで実運用向けに広げたかを扱います。
