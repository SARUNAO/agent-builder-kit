# Fact Report Template

下流から上流へ返す事実だけの報告。  
解釈や次の方針決定は上流側で行う。

`BLK-007` 以降は、必要に応じて `decision / gotcha / command / before-after` に再利用できる粒度で残す。  
ただし毎回すべてを長文で埋める必要はなく、「今回の ticket で残す価値がある事実」だけを短く書く。

```md
# Fact Report: {ticket title}

- ticket_id: TICKET-YYYY-MM-DD-XXX
- author: タスクワーカー
- submitted_on: YYYY-MM-DD

## 変更したファイル
- `path/to/file`

## 実行したコマンド
- `cargo test ...`
- `pnpm test ...`

## 結果
- 成功した検証
- 失敗した検証
- 未実施の検証

## 記録素材メモ
- decision:
  - 今回の ticket で確定した判断
- gotcha:
  - 詰まりどころ、環境依存、回避策
- command:
  - 再利用価値のあるコマンドと、その結果の要約
- before / after:
  - 変更前後で何が増えたか、どう変わったか

## reviewer 結果
- findings の有無
- 対応したかどうか

## 未解決事項
- 現時点で残っている事実ベースの懸念

## scope breach
- なし
- ある場合は、どこまで広がったか

## 補足
- 次 ticket に渡すべき事実
- 本文や一次記録 docs へ再配置しやすい短いメモ
```

## 書き方の目安
- `結果` は事実だけを書く
- `記録素材メモ` は、後で `docs/exec-plans/active/` へ移しやすい短文にする
- `decision` と `gotcha` がなければ `なし` でよい
- `before / after` は diff 全文ではなく、読者向けに使える変化だけを書く
