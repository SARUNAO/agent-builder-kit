# task-worker で ticket を実行し、fact-report を返す

`task-planner` が chunk と ticket を切ったら、次に実際に手を動かすのが `task-worker` です。
この role は、計画そのものを書き換えるのではなく、与えられた ticket の範囲だけを実装し、その結果を事実として返します。

## task-worker の役割

`task-worker` が最初に見るのは、ticket の `Goal`, `editable_paths`, `Verification` です。
つまり「何を達成するか」「どこを触ってよいか」「何をもって完了とみなすか」を見てから作業に入ります。

ここで重要なのは、勝手に plan を拡張しないことです。
必要な変更が ticket の外へはみ出しそうなら、無理に進めず、ticket レベルで上流へ返します。

言い換えると `task-worker` は、実装担当であると同時に、境界を守る担当でもあります。

## task-worker の使い方

呼び出し方はこれまでの role と同じで、Codex アプリから Skill を選ぶだけです。
この project でも、各 ticket を進めるたびに `task-worker` を呼び出し、対象 ticket の範囲だけを実行していきました。

たとえば `TICKET-002` では、次のような仕事を受け持っています。

- `mdbook init` を実行する
- `book.toml` と `src/` の生成物を確認する
- 次の ticket が使いやすいよう、日本語の最小スタブへ整える

ここでは `editable_paths` が `book.toml` と `src/` に限定されていたため、`task-worker` はその範囲だけを更新しています。

## 実装した結果をどう返すか

`task-worker` は、ファイルを変更して終わりではありません。
実装後は、ticket 本文の実施結果を埋め、さらに `fact-report` を返します。

`fact-report` には、少なくとも次のような事実が残ります。

- 何の ticket を実行したか
- どのファイルを変えたか
- どのコマンドを打ったか
- 何が起きたか
- 未解決事項があるか

これがあると、人間はあとから「何をしたのか」を会話ログに頼らず追えます。
同時に、次の role もその ticket の結果を一次記録として再利用できます。

今回の project でも、`TICKET-002` の `fact-report` には、`mdbook init --force --title "mdBook Workshop" .` を実行して最小骨格を作ったことや、`book.toml`, `src/SUMMARY.md`, `src/overview.md` が生成されたことが残っています。

## reviewer が入るとき

`reviewer` は独立した章にはしませんが、`task-worker` の流れの中で重要な役目です。
コードや設定を実際に変更した ticket では、`task-worker` は実装後に `reviewer` へ handoff します。

この project では、`TICKET-002` がその例です。
`book.toml` と `src/` の実ファイルを更新しているため reviewer 対象になり、結果として no findings で通過しました。

一方、docs の更新と確認だけで終わる ticket では、毎回 reviewer を通す必要はありません。
たとえば `TICKET-004` では、`mdbook build` と `mdbook serve --open` の確認結果を README と fact-report に残す作業が中心だったため、`docs-only skip` として扱われています。

この切り分けがあることで、review を必要な場所へ集中できます。

## 結果を上流へ返し、status を昇華させる

`task-worker` が結果を返したら、それで終わりではありません。
返ってきた ticket 本文、`fact-report`、review 結果を見て、次に `task-planner` が ticket を `done` へ上げます。

さらに、chunk 配下の ticket がすべて `done` になれば、`task-planner` は chunk close の材料をそろえます。
そのあと `plan-manager` が全体の進み方を見て、必要なら block の status も引き上げます。

つまり流れとしては、次のようになります。

- `task-worker` が ticket を実行する
- `fact-report` と review 結果を返す
- `task-planner` が ticket を `done` に昇格させる
- 配下がそろえば chunk を閉じる
- さらに上流では `plan-manager` が block の進捗を判断する

この流れがあることで、変更は単発で終わらず、開発フロー全体の進捗へ接続されます。
`task-worker` の返却物が大事なのは、そのまま上流の status 更新の根拠になるからです。

## 返ってくるものは変更だけではない

`task-worker` が返すのは、差分だけではありません。
実行したコマンド、確認結果、未解決事項、review の扱いまで含めて返すことで、あとから見た人が「どこまで終わっていて、何が残っているか」を判断しやすくなります。

だからこの role の本質は、単に実装することではなく、「実装を追跡可能な形で返すこと」にあります。

ここまでできると、task ごとの結果が一次記録として積み上がり、あとからチュートリアル本文へ再構成しやすくなります。
この project でも、`task-worker` が返した `fact-report` が、そのまま次の章づくりの根拠になっています。
