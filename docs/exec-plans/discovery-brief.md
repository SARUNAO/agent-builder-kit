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
- `book.toml`, `src/SUMMARY.md`, `src/*.md` など mdBook 本体はまだ未作成である
- 現在の repo 実体は docs / skill / canvas 中心で、実装 block へは未着手である
- GitHub へ公開し、ワークショップまたはチュートリアルとして使える状態までを初回ゴールに含める
- `agent-builder-kit` は現在 repo 直下に存在せず、必要時に別途持ち込む前提である
- 2026-03-10 時点のこの環境では `mdbook` コマンドが未導入である
- 章構成は増える可能性があるが、章内の目次で吸収しながら進めてよい

## 仮置き前提
- 最初の骨格は mdBook の最小構成と 3 から 4 章程度の記事で立ち上げ、必要に応じて章内目次で拡張する
- 参加者に見せたい主眼は mdBook 単体ではなく、agent-builder の開発フロー体験である
- Rust と cargo は利用可能、または導入手順をワークショップ内で案内する
- mdBook の初期化は公式ガイドに沿って `mdbook init` を第一候補にする
- ローカル確認は `mdbook serve --open` を使い、CI の基本ゲートは `mdbook build` に置く
- Rust コード例を本文へ入れる場合だけ `mdbook test` を追加し、link check は publish block で optional に判断する
- GitHub 公開は GitHub Pages と GitHub Actions を第一候補にする
- 章構成は「概要」「環境確認」「role フロー体験」「最初の mdBook 更新」の 4 章前後を第一候補とする

## 非目的
- 最初から凝ったテーマや高度なカスタム UI を作ること
- 記事の全章を一度に完成させること
- 動画配信や外部 CMS 連携まで扱うこと

## 制約
- block -> chunk -> ticket の流れをワークショップ中に追えるようにする
- canvas を見ながら進捗を説明できるようにする
- 参加者が agent ごとの役割を理解できるよう、Human Manual と README の導線を保つ
- `agent-builder-kit` が repo 直下にないため、publish block では取得方法や配置を明示する必要がある
- `mdbook` コマンド未導入のため、骨格作成 block では導入手順または前提整理が必要になる

## 未確定事項
- GitHub 上で `agent-builder-kit` と mdBook を同一 repo / 別 repo のどちらで公開するか
- 公開先を GitHub Pages の project site にするか、別ホスティングを併用するか
- link check や追加 lint を初回 publish から必須化するか

## 現時点の推奨案
- 推奨: `mdbook init` で最小骨格を起こし、`mdbook serve --open` でローカル確認しつつ、GitHub Pages への Actions deploy を publish block で入れる
- 理由: mdBook 公式ガイドの入口に沿いやすく、GitHub の公式運用とも接続しやすい
- 代替案: 手動で最小ファイルを作る案は構造理解には良いが、初回は導入ミスが増えやすい。別ホスティング先を先に選ぶ案は公開判断が増えすぎる
