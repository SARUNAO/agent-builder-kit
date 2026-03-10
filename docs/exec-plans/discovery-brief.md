# Discovery Brief

- discovery_id: DISCOVERY-2026-03-10
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- status: done
- last_updated: 2026-03-10

## 確定事項
- 対象は何もない新規リポジトリである
- 成果物は mdBook のワークショップ記事サイトである
- ワークショップの中で agent-builder 自体の使い方も体験させる
- docs 駆動の workspace と planning 環境は生成済みである
- `book.toml`, `src/SUMMARY.md`, `src/*.md` の最小骨格は作成済みである
- `mdbook v0.5.2` は導入済みである
- `mdbook build` は成功済みで、`book/` に HTML を生成できる
- `mdbook serve --open` は通常ローカルでは起動確認できるが、sandbox では localhost bind 制約がある
- GitHub へ公開し、ワークショップまたはチュートリアルとして使える状態までを初回ゴールに含める
- `agent-builder-kit` は現在 repo 直下へ配置済みである
- 章構成は増える可能性があるが、章内の目次で吸収しながら進めてよい
- mdBook の主題には、いま進めている開発プロセスそのものも含まれる
- 後から主観で書き直すのではなく、作業中から客観的な一次記録を回収する必要がある
- 一次記録の置き場は、まず `docs/exec-plans/` 配下へ寄せる方針で進める
- BLK-003 では、mdBook 入門を前面に出すより `agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングの tutorial 性を強めたい
- 本文の比重は mdBook 3、`agent-builder-kit` / 開発フロー 7 程度を目安にしたい
- 文体は現在の planning docs より少しやわらかくし、硬さ 10 に対して 7 程度を狙う
- GitHub 公開は `agent-builder-kit` と mdBook を同一 repo で進める
- 公開先は GitHub Pages を使う
- link check は初回 publish の必須ゲートにせず、publish 後の改善項目として扱う

## 仮置き前提
- 最初の骨格は mdBook の最小構成と 3 から 4 章程度の記事で立ち上げ、必要に応じて章内目次で拡張する
- 参加者に見せたい主眼は mdBook 単体ではなく、agent-builder の開発フロー体験である
- Rust と cargo は利用可能、または導入手順をワークショップ内で案内する
- mdBook の初期化は公式ガイドに沿って `mdbook init` を第一候補にする
- ローカル確認は `mdbook serve --open` を使い、CI の基本ゲートは `mdbook build` に置く
- Rust コード例を本文へ入れる場合だけ `mdbook test` を追加し、link check は publish 後の改善項目として判断する
- GitHub 公開は GitHub Pages と GitHub Actions を採用する
- 章構成は「概要」「環境確認」「role フロー体験」「最初の mdBook 更新」の 4 章前後を第一候補とする
- 記事本文の前に、開発中の判断・コマンド・詰まり・差分を素材として残す block を置く
- 一次記録は command / decision / gotcha / before-after を基本単位とし、全文ログやスクリーンショットは必須にしない
- BLK-003 では mdBook を主役にせず、`agent-builder-kit` の運用実例として mdBook を使う構図を基本にする
- `ハーネスエンジニアリング` という語は使ってよいが、初見読者向けに短い言い換えや補足を添える

## 非目的
- 最初から凝ったテーマや高度なカスタム UI を作ること
- 記事の全章を一度に完成させること
- 動画配信や外部 CMS 連携まで扱うこと
- 記憶頼みで後から体験談を再構成すること
- mdBook の一般的な入門書として網羅解説すること

## 制約
- block -> chunk -> ticket の流れをワークショップ中に追えるようにする
- canvas を見ながら進捗を説明できるようにする
- 参加者が agent ごとの役割を理解できるよう、Human Manual と README の導線を保つ
- `agent-builder-kit` が repo 直下へ配置されたため、publish block では同一 repo 内での配置と公開導線を前提に整理する必要がある
- チュートリアル本文は、作業時点の一次記録と矛盾しないことが求められる
- sandbox では `mdbook serve --open` の挙動が再現しない場合があるため、ローカル端末確認を正として区別する必要がある
- 文体をやわらかくしても、判断根拠や事実の粒度は落としすぎない

## 未確定事項
- GitHub Pages を project site として公開する場合の repository 名と公開 URL の置き方
- GitHub Actions の publish で `mdbook build` 以外にどこまで確認を含めるか

## 現時点の推奨案
- 推奨: `mdbook init` で最小骨格を起こし、`mdbook serve --open` でローカル確認しつつ、GitHub Pages への Actions deploy を publish block で入れる
- 理由: mdBook 公式ガイドの入口に沿いやすく、GitHub の公式運用とも接続しやすい
- 代替案: 手動で最小ファイルを作る案は構造理解には良いが、初回は導入ミスが増えやすい。別ホスティング先を先に選ぶ案は公開判断が増えすぎる
- 推奨: `BLK-002` の直後に、decision log / gotcha log / command log / before-after を回収する専用 block を差し込む
- 理由: 記事本文を書き始める前に一次資料の置き場を決めておくと、後から主観で補完する量を減らせる
- 代替案: 記録を本文作成 block に吸収する案はあるが、事実と読者向け文章が混ざりやすい
- 推奨: 一次記録は `docs/exec-plans/` 配下に寄せ、公開時に必要な粒度へ要約する
- 理由: source of truth を planning docs 側に固定でき、mdBook 本文へ後から再配置しやすい
- 代替案: mdBook 本文に直接下書きを混ぜる案はあるが、一次記録と読者向け文章の境界が曖昧になりやすい
- 推奨: BLK-003 は `agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングを主軸にし、mdBook は具体例として従属させる
- 理由: この repo の独自性は mdBook 自体より、どういう開発フローで成果物を作ったかにあるため
- 代替案: mdBook 初学者向けに主題を寄せる案は分かりやすいが、`agent-builder-kit` の tutorial としての価値が薄くなりやすい
- 推奨: 初回 publish は GitHub Pages + GitHub Actions + `mdbook build` を最小ゲートとして進め、link check は公開後の改善項目に回す
- 理由: まず公開導線を閉じるほうが重要で、初回から検査項目を増やしすぎると publish block が停滞しやすい
- 代替案: 初回から link check や追加 lint を必須にする案は品質面では強いが、現段階では公開導線の確立を優先したほうが進行が安定する
