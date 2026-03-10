# はじめに

ようこそ、Agent-builder-kit のチュートリアルへ。

この mdBook は、`agent-builder-kit` で構築した `AGENTS.md` と `docs/` を土台に作成しました。この過程を記録し、実際の成果物へどのように着手し、どう進めたかをチュートリアル形式で見てもらうことで、この mdBook の開発フローを追体験してもらうことが目的です。

制作および開発フローは、`plan-manager` が block を決め、`task-planner` が chunk と ticket に落とし、`task-worker` が実装し、必要なら `reviewer` が確認する流れになります。

## このチュートリアルで扱うこと

- `agent-builder-kit` を前提にした docs 駆動の進め方
- `AGENTS.md` と `docs/exec-plans/` を使った役割分担
- mdBook を題材にした最小成果物の立ち上げと記録の残し方
- Obsidian の `.canvas` と連携した開発フローの視覚化
- ハーネスエンジニアリングの一部である、タスクの細分化と境界分離の進め方

## このチュートリアルで扱わないこと

- mdBook の全機能を網羅すること
- 一般的な AI 開発論だけを抽象的に語ること
- ハーネスエンジニアリングで語られる CI、カスタムリンター、厳密な境界分離を支えるレイヤードアーキテクチャを、この段階で詳細に実装し切ること

mdBook はここでは器です。器を作りながら、`agent-builder-kit` と、その土台にある docs 駆動開発 / ハーネスエンジニアリングの実際を一緒に確認していきます。

## 参考記事

- [「人間はコードを1行も書かない」という縛りで5ヶ月間プロダクトを作り続けた結果 ― ハーネスエンジニアリング | Qiita](https://qiita.com/nogataka/items/43c01957fa1e54d9a079)
- [ハーネスエンジニアリング：エージェントファーストの世界における Codex の活用 | OpenAI](https://openai.com/ja-JP/index/harness-engineering/)
