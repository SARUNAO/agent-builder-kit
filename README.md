# mdBook Workshop

AI コーディング前提の開発フローを運用するための docs 駆動 workspace。

## 最初に理解しておくこと
- init 後に `agent-builder-kit/` を削除した場合、展開元 package の docs や相対パスはもう前提にしない
- Codex アプリを再起動して project を開き直したあとの AI は、bootstrap 前や直前セッションの文脈を持っていない前提で扱う
- そのため、この repo の作業は毎回 `AGENTS.md` と `docs/` を読み直すところから始める

## Codex アプリでの再開手順
1. いまのスレッドを閉じる
2. Codex アプリを再起動する
3. この project を新しい project として開き直す
4. 新しいセッションの AI に、まず `AGENTS.md`, `docs/index.md`, `docs/PLANS.md`, `docs/HUMAN_MANUAL.md` を読むよう依頼する
5. その後で `plan-manager` から作業を始める

## 入口
- `AGENTS.md`
- `docs/index.md`
- `docs/HUMAN_MANUAL.md`
- `docs/PLANS.md`
- `docs/ROLE_SKILLS.md`

## runtime artefact
- planning: `docs/exec-plans/plan-spec.md`, `docs/exec-plans/blocks`
- canvas: `docs/exec-plans/canvas/development-flow.canvas`
- canonical skill source: `tools/codex-skills/`
- user-facing skill export: `.agents/skills/`

## 進め方
- `plan-manager` に目的と追加要件を伝える
- `task-planner` に chunk / ticket を切ってもらう
- `task-worker` と `reviewer` で実装と確認を進める
