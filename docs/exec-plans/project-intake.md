# Project Intake

- intake_id: INTAKE-2026-03-10
- parent_plan: PLAN-2026-03-10-MDBOOK-WORKSHOP
- status: captured
- last_updated: 2026-03-10

## 要求原文
- 何もない新規リポジトリから、agent-builder を使って mdBook のワークショップ記事サイトを作りたい。ワークショップ自体で plan-manager -> task-planner -> task-worker の流れも体験できるようにする。

## 追加ヒアリング
- 2026-03-10: 環境構築は完了している
- 2026-03-10: まだ mdBook 本体や記事コンテンツは作っていない
- 2026-03-10: ゴールは GitHub で `agent-builder-kit` と mdBook を公開し、ワークショップまたはチュートリアルとして機能する状態まで含む
- 2026-03-10: `agent-builder-kit` は当初この repo 直下になかったが、現在はルート下へ配置済みである
- 2026-03-10: この mdBook に書く主題は、いま実際に進めている開発プロセスそのものでもある
- 2026-03-10: 後で客観的に記事化できるよう、作業中から事実ベースの記録を残したい
- 2026-03-10: 次 block は記録基盤整備を優先し、本文作成より先に一次記録の置き場を整える
- 2026-03-10: BLK-003 では、mdBook 入門を前面に出しすぎず、`agent-builder-kit` と docs 駆動開発 / ハーネスエンジニアリングの tutorial 性を主軸にしたい
- 2026-03-10: 内容配分は mdBook 側 3、`agent-builder-kit` / 開発フロー側 7 を目安に寄せたい
- 2026-03-10: 文体は現在の planning docs より少しやわらかくし、硬さ 10 に対して 7 程度を目安にしたい
- 2026-03-10: GitHub 公開は `agent-builder-kit` と mdBook を同一 repo で進める
- 2026-03-10: 公開先は GitHub Pages を使う
- 2026-03-10: link check は初回 publish の必須ゲートにせず、publish 後の改善項目として扱う

## 明確化された目的
1. agent-builder-kit の実運用テストと、その記録を残す
2. みんなに使ってもらうためのチュートリアルを作る
3. mdBook を、AI と docs 駆動フローで作る題材として使う
4. 実際の開発中に起きた判断、詰まり、解決を一次資料として回収する
5. `agent-builder-kit` の設計思想と、その土台にある docs 駆動開発 / ハーネスエンジニアリングの入口を伝える

## 成果物候補
- mdbook_site
