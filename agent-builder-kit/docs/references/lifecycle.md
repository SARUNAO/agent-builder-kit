# ライフサイクル

## 標準フロー
1. `プランオーナー` が人間からの要求を `project-intake` に記録する
2. `プランオーナー` が確認事項、仮置き前提、非目的を `discovery-brief` に整理する
3. `プランオーナー` が `discovery-brief` を元に `plan-spec` を固める
4. `タスクプランナー` が `plan-spec` を `chunk-sheet` と `ticket` に分解する
5. `タスクワーカー` が ticket を実装し、review を通す
6. `タスクプランナー` が task 完了を集約し、chunk を閉じる準備をする
7. `reviewer` が chunk review を行う
8. chunk close で docs 同期、commit、次 chunk 解放可否を判断する
9. `プランオーナー` が program board の進捗を更新する

## 5 役へ拡張したときの読み替え
- `プランオーナー` の仕事を `プランマネージャー` と `仕様設計者` に分割する
- `プランマネージャー` は `program-board` と優先順位付けを持つ
- `仕様設計者` は `project-intake`, `discovery-brief`, `plan-spec` の主担当を持つ

## 上流から下流への流れ
- `program-board`
  - 今どのプランを進めるか
- `project-intake`
  - 人間要求の原文と初期論点
- `discovery-brief`
  - 仮置き前提、未確定事項、MVP、非目的
- `plan-spec`
  - 何を作るか
- `chunk-sheet`
  - どう分けて進めるか
- `ticket`
  - 今回何をやるか

## 下流から上流への流れ
- `fact-report`
  - 実際に変わったこと
- task review result
  - 局所的な問題
- chunk review result
  - 統合上の問題

## chunk を置く理由
- task 単位だと局所最適に寄りやすい
- plan 単位だと大きすぎて commit と docs 同期が遅い
- 2-5 task 程度のまとまりを中間単位にすると、統合レビューと進捗更新の粒度が揃う

## なぜ `project-intake` と `discovery-brief` を置くか
- 人間要求は最初から仕様ではない
- 要求原文と採用仕様を混ぜると、後で何が要望で何が仮定だったか崩れる
- `タスクプランナー` が曖昧な要求を背負うと、ticket のやり直しが増える

## 推奨粒度

### project-intake
- ユーザー要求の原文を崩さずに残す入口
- 期間は最初の会話 1 回分でもよい

### discovery-brief
- 要求を仕様化できる形へ整理する短い docs
- 人間確認前の仮置き前提もここに集約する

### plan
- 1 つの目的を達成する中規模テーマ
- 期間は数日から数週間

### chunk
- 2-5 task を束ねる統合単位
- 1 回の包括 review と 1 回の commit 区切り

### ticket
- 1 ワーカーが独立して完了できる単位
- `editable_paths` を明確に切れる大きさ

## エスカレーション条件
- `project-intake` の時点で成果物の種類が定まらない
- `discovery-brief` の時点で MVP や非目的が定まらない
- `plan-spec` で仕様が固まらない
- ticket 化すると ownership が競合する
- reviewer findings により plan の前提が崩れた
- chunk review で統合リスクが高いと判明した

この場合は上流役が人間へ戻す。標準 4 役では `プランオーナー`、拡張 5 役では `プランマネージャー` が持つ。
