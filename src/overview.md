# agent-builder-kit の導入

まずは `agent-builder-kit` を用意します。公開後はここに GitHub の公開 repo リンクを置く予定です。

> 現在はまだ公開前です。GitHub へ公開したあとで、この導線は同一 repo の実 URL に差し替えてください。

## 新規プロジェクトを開始

Codex アプリで新規プロジェクトを立ち上げ、空のルートディレクトリを用意します。

Obsidian をまだ導入していない場合は、この段階で先に入れておきます。
公式サイトから Obsidian をインストールし、起動後に `Open folder as vault` を選んで、この project のルートディレクトリを Vault として開いてください。

Obsidian で project を開くと `.obsidian/` が生成され、`.canvas` を使った開発フローの可視化も扱えるようになります。

`agent-builder-kit` を使った初期化では、次の 3 つがルート下に並ぶ状態から始めます。

```text
.
├── .obsidian/
├── agent-builder-kit/
└── docs-builder.toml
```

- `.obsidian/`: ノートアプリの Obsidian でこのプロジェクトを Vault として開くと生成されるファイルです。`agent-builder-kit` には `.canvas` と同期する Skill が同梱されており、開発フローを視覚化するコア機能でもあるため、Obsidian との連携を強くおすすめします。
- `agent-builder-kit/`: `AGENTS.md` や構造化した `docs/` を初期テンプレートとして展開するパッケージです。
- `docs-builder.toml`: builder が読み込む設定ファイルです。生成する docs 構成、planning layout、profile、add-on pack はこのファイルで決まります。`agent-builder-kit` 内にある `docs-builder.toml.example` を、プロジェクトに合わせて編集してからルート下へ配置してください。

Obsidian の準備としては、ここで Vault として開ければ十分です。
`.canvas` の見方や、planning docs とどう同期されるかは後続の chapter で扱います。

## パッケージの展開

Codex セッションを開始し、エージェントに `agent-builder-kit` を展開してもらいましょう。

例:
```text
agent-builder-kit/PACKAGE_CONTENTS.mdと
agent-builder-kit/README.mdを読んでガイドに従ってください
```

展開が済むと、元のパッケージである `agent-builder-kit` を削除するか残すか尋ねられると思うので、不要であれば削除してください。

```text
.
├── .agents/
├── .obsidian/
├── agent-builder-kit/
├── docs/
├── tools/
├── AGENTS.md
├── docs-builder.toml
└── README.md

```

準備はほぼ整いました！

ただし最後の注意点として、Codex アプリでは現在、セッションを開始した後に生成された Skill が即座に反映されないため、一度セッションを閉じて削除してから Codex アプリを再起動し、その後 `新しいプロジェクトの追加` を行って新しいセッションを立ち上げるようにしてください。

`$` コマンドで次の Skill が候補に上がれば、準備は完了です。
```text
Obsidian Canvas Sync
Plan Manager
Reviewer
Task Planner
Task Worker
```
これらのSkillを実際にどう使うかは後述のチャプターでお見せします。

公開後は、この mdBook 自体も同じ repo の GitHub Pages から読めるようになります。
つまり読者は、repository と tutorial site を行き来しながら `agent-builder-kit` と本文の両方を追える構成になります。

## 注意点

<br>
・すでにプロジェクトが進行中の場合

`AGENTS.md` および `docs/` が存在するプロジェクトにおいては、`docs-builder.toml` を以下にすることで統合モードで展開できます。
```toml
[project]
mode = "migration"
```
ただし、すでに十分な `.md` が存在しドキュメントが膨大な場合は、完全な移行ができない恐れがあります。その場合は閉じたフォルダ下に展開したうえで現行 `docs/` をバックアップし、移行タスクを細分化した上で進めてください。実験的な `mode` であるため、動作は保証できません。

<br>
・Claude環境下

未定義であるため保証できませんが、実体は Markdown と Python script 中心であるため、強依存はなく `CLAUDE.md` や `tools/codex-skills/` に対する手動による最適化を行えば機能する見込みです。

<br>
・WSL環境でのObsidian

Windows 側の Obsidian から WSL 上のプロジェクトフォルダへは直接アクセスすることはできません。Linux 版 Obsidian をインストールし、WSLg で動作させてください。

[Windows11 + WSL で Obsidian を快適に使うまでの試行錯誤 | Zenn](https://zenn.dev/saetag/articles/7a2b3c1f15e9f9)
