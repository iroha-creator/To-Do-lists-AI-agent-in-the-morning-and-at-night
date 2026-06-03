# To-Do-lists-AI-agent-in-the-morning-and-at-night
An AI agent that creates and reviews to-do lists twice a day, taking user feedback into account

# TodoAgent

朝と夜の2回、AIと会話しながらTo-Doリストを作成・確認するエージェントです。

---

## 機能

- 🌅 **朝セッション** — その日のタスクをAIと一緒に整理
- 🌙 **夜セッション** — 完了したタスクを確認・記録
- 💬 **自然な会話形式** — Gemini APIによる対話でタスクを柔軟に追加・更新
- ⏰ **自動起動** — Windowsタスクスケジューラーで設定時刻に自動起動

---

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [SETUP.md](./SETUP.md) | 初回セットアップ手順 |
| [SCHEDULER_SETUP.md](./SCHEDULER_SETUP.md) | Windowsタスクスケジューラー登録手順 |

---

## ファイル構成

```
todo_agent/
├── main.py               # エントリーポイント
├── agent.py              # Gemini APIとの対話処理
├── todo_manager.py       # To-Doデータの読み書き
├── scheduler.py          # 時刻トリガーの管理
├── requirements.txt      # 依存ライブラリ
├── .env.example          # 環境変数のテンプレート
├── .gitignore
├── README.md
├── SETUP.md
└── SCHEDULER_SETUP.md
```

---

## クイックスタート

```bash
# 1. ライブラリのインストール
pip install -r requirements.txt

# 2. .envの作成
copy .env.example .env   # Windowsの場合

# 3. 動作確認
python main.py --morning
```

詳細は [SETUP.md](./SETUP.md) を参照してください。

---

## 使用技術

- Python 3.10+
- [Google Gemini API](https://aistudio.google.com/)
- [schedule](https://schedule.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)