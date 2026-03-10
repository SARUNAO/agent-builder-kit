# Article Source Map

この docs は、BLK-003 の本文作成でどの一次記録を章の根拠に使うかを一覧化するための素材マップ。

## 使い方
- 章本文そのものはここに書かない
- まず章ごとの根拠を見つけ、足りない記録があれば別 ticket で補う
- 参照先は `docs/exec-plans/active/` と `fact-report` を優先する
- root `asset/` のスナップショットは、内容断定ではなくファイル名ベースの補助素材として使う

## agent-builder-kit の導入
- 章のねらい:
  - 新規プロジェクトで `agent-builder-kit` をどう配置し、Obsidian とあわせてどこから初期化を始めるかを最初に説明する
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-011-agent-builder-kit-intro-draft.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-025-obsidian-setup-guide-draft.md`
  - `docs/exec-plans/active/before-after.md`
- 補助アセット:
  - `asset/agent-builder-kit展開前プロジェクトルート下ディレクトリ.png`
  - `asset/plan-managerが生成したブロックを基にtask-plannerがチャンクとタスクチケットを生成.png`
- 使えそうな事実:
  - Obsidian は先に導入し、project ルートを Vault として開けばよい
  - 最初にルートへ `.obsidian/`, `agent-builder-kit/`, `docs-builder.toml` を置く
  - `docs-builder.toml.example` をプロジェクト向けに編集してから配置する
  - Codex アプリでは Skill 反映のため再起動が必要になる場合がある
  - 公開後は、同一 repo の GitHub Pages と repository を行き来しながら読む構成になる
- 足りない記録:
  - GitHub 公開後の実 URL はまだない
  - `docs-builder.toml` の具体例と profile 選択理由はまだ本文に入っていない
  - Obsidian の OS ごとの詳細導入手順は、この章では扱っていない

## plan-manager でプロジェクトの骨子を組む
- 章のねらい:
  - `plan-manager` が project の骨子をどう組み立てるかを最初の planning 行為として説明する
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-013-plan-manager-skeleton-draft.md`
  - `docs/exec-plans/project-intake.md`
  - `docs/exec-plans/discovery-brief.md`
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/blocks/block-003-workshop-content.md`
- 補助アセット:
  - `asset/初回plan-manager実行後に生成された開発フロー.png`
- 使えそうな事実:
  - `plan-manager` は要求整理と上流計画更新を担当する
  - `project-intake`, `discovery-brief`, `plan-spec`, block note がこの段階の主な生成物になる
  - まず block で骨子を作り、その後で `task-planner` が chunk / ticket へ分解する
- 足りない記録:
  - block をどう差し込んで再編したかの実例は、後続推敲で補う余地がある
  - `.canvas` 画像をどの粒度で本文に埋め込むかは、後続推敲で再判断する

## task-planner で仕事を chunk と ticket に分ける
- 章のねらい:
  - `task-planner` が block を chunk / ticket へどう分解し、必要に応じて再計画を差し込むかを追体験させる
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-015-task-planner-breakdown-draft.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-001-mdbook-prereq.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-002-mdbook-init.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-003-summary-and-stubs.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-004-local-verification.md`
  - `docs/exec-plans/active/decision-log.md`
- 補助アセット:
  - `src/images/before_chunk.png`
  - `src/images/after_chunk.png`
  - `src/images/planner_chunk.png`
  - `src/images/planner_chunk2.png`
- 使えそうな事実:
  - `task-planner` は block を chunk と ticket に分解し、`task-worker` が動ける粒度へ落とす
  - `Goal`, `editable_paths`, `Verification` が ticket の最小骨格として機能する
  - 配下 ticket 完了後に、現在の block へ chunk を差し込むか、上流 block へ戻すかを判断する
  - `.canvas` を見ると、block だけの状態から chunk / ticket へ広がる流れが追いやすくなる
- 足りない記録:
  - `task-planner` が block 単位へ戻す判断を実際に返した会話ログは、本文ではまだ一例だけに留まっている
  - chapter file path `src/role-flow.md` を章タイトルに合わせて変えるかは未確定

## task-worker で ticket を実行し、fact-report を返す
- 章のねらい:
  - `task-worker` が ticket をどう実行し、`fact-report` と review 扱いまで含めて何を返すかを具体的に見せる
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-017-task-worker-execution-draft.md`
  - `docs/exec-plans/active/before-after.md`
  - `docs/exec-plans/active/command-log.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-002-mdbook-init.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-004-local-verification.md`
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-003-summary-and-stubs.md`
- 補助アセット:
  - 必要なら後続 ticket で追加
- 使えそうな事実:
  - `task-worker` は `Goal`, `editable_paths`, `Verification` を見て ticket を実行する
  - 実装後は ticket 本文だけでなく `fact-report` でも事実を返す
  - コードや設定変更がある ticket では reviewer handoff が入り、docs-only ticket では skip できる
  - `TICKET-002` は reviewer 対象、`TICKET-004` は docs-only skip の実例になる
  - `task-worker` の返却物は、そのまま `task-planner` の ticket `done` 判定と chunk close の根拠になる
  - さらに上流では `plan-manager` が block の進捗判断へ接続する
- 足りない記録:
  - `fact-report` の見た目そのものを示す図版はまだない
  - chapter file path `src/first-change.md` を章タイトルに合わせて変えるかは未確定

## 開発ログからチュートリアル本文を組み立てる
- 章のねらい:
  - planning docs、fact-report、active logs をどう本文へ再構成するかを説明し、この project の開発記録を教材へ変換する流れを見せる
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-019-log-to-article-draft.md`
  - `docs/exec-plans/active/index.md`
  - `docs/exec-plans/active/decision-log.md`
  - `docs/exec-plans/active/gotcha-log.md`
  - `docs/exec-plans/active/command-log.md`
  - `docs/exec-plans/active/before-after.md`
  - `docs/exec-plans/active/article-source-map.md`
- 補助アセット:
  - 必要なら後続 ticket で追加
- 使えそうな事実:
  - planning docs、fact-report、active logs は役割ごとに分かれており、その分け方自体が本文の材料になる
  - いきなり本文を書かず、source map を一段挟むことで、根拠のない文章化を避けやすい
  - 実際の作業順と読者向けの説明順はずれてよく、その対応づけを source map が支える
  - この章自体も AI エージェント側の提案で差し込まれたため、開発フローそのものを題材化している
- 足りない記録:
  - この章に対応する図版はまだない
  - chapter file path `src/process-to-article.md` を将来変更するかは未確定

## 真のハーネスエンジニアリングへ至るには？
- 章のねらい:
  - 現在の `agent-builder-kit` の到達点と限界を整理し、マルチエージェント化、CI/CD、lint、境界設計支援などの拡張候補を読者へ示す
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-021-true-harness-engineering-draft.md`
  - OpenAI の Harness Engineering 記事
- 補助アセット:
  - 必要なら後続 ticket で追加
- 使えそうな事実:
  - 今の kit は docs と role 境界の固定まではできているが、マルチエージェント並列実行や自動検証までは標準で持っていない
  - CI/CD、lint、レイヤードアーキテクチャ支援は project 依存が強いため、汎用性を優先して kit には標準同梱していない
  - `.canvas` の色分けや専用 Skill の追加によって、さらに本格的な harness engineering へ拡張できる
  - `agent-builder-kit` は大半が `.md` docs で構成されているため、利用者自身が拡張しやすい
- 足りない記録:
  - 並列化や CI/CD add-on の具体仕様はまだ構想レベル
  - chapter file path `src/true-harness-engineering.md` は新設済みだが、図版や実装例はまだない

## おわりに
- 章のねらい:
  - ワークショップ全体を短く総括し、`agent-builder-kit` の価値、今の限界、読者が次に試す一歩を自然につなげる
- 主な根拠:
  - `docs/exec-plans/fact-reports/fact-report-2026-03-10-ticket-023-conclusion-draft.md`
  - `docs/exec-plans/plan-spec.md`
  - `docs/exec-plans/active/article-source-map.md`
- 補助アセット:
  - 必要なら後続 ticket で追加
- 使えそうな事実:
  - この mdBook 自体が `agent-builder-kit` を使った実例として最後まで組み上げられた
  - 人間と AI エージェントが同じ docs を見ながら進めることが、この flow の中心的な価値になっている
  - 並列実行、CI/CD、lint、厳密な境界設計は今後の拡張余地として残っている
  - 読後の次の一歩は、kit を自分の project に展開し、小さな成果物で block / chunk / ticket を回してみること
  - 公開後は tutorial site と同一 repo の `agent-builder-kit` を行き来しながら参照できる
- 足りない記録:
  - 実運用をさらに継続したあとの長期的な振り返りはまだない
  - chapter file path `src/conclusion.md` は現状のままで問題ないが、公開時に章名変更の可能性はある

## BLK-003 へ渡すメモ
- まずはこのマップを見て、章ごとにどの根拠をどの順番で使うかを決める
- 記録不足は本文で埋めず、必要なら追加 ticket で回収する
- `src/` の本文は、この docs を索引として使ってから書き始める
