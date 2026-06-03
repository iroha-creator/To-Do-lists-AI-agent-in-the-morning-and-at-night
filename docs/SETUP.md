# セットアップ手順

---

## 前提条件

以下がインストールされていること。

- Python 3.10以上 → [python.org](https://www.python.org/downloads/)
- VS Code → [code.visualstudio.com](https://code.visualstudio.com/)

バージョン確認:

```bash
python --version
pip --version
```

---

## 手順

### 1. プロジェクトフォルダの作成

任意の場所に `todo_agent` フォルダを作成します。

---

### 2. ファイルの配置

以下のファイルをすべて `todo_agent` フォルダに配置します。

```
todo_agent/
├── main.py
├── agent.py
├── todo_manager.py
├── scheduler.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

### 3. VS Codeでフォルダを開く

**方法A（推奨）:** `todo_agent` フォルダを右クリック →「Codeで開く」

**方法B:** VS Code起動 → `ファイル` → `フォルダーを開く` → `todo_agent` を選択

---

### 4. 仮想環境の作成・有効化

VS Codeのターミナル（`Ctrl + @`）を開き、以下を実行します。

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\Activate.ps1
```

```bash
# Mac / Linux
source .venv/bin/activate
```

成功すると行頭に `(.venv)` が表示されます。

> PowerShellでエラーが出る場合:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> を実行してから再度試してください。

---

### 5. ライブラリのインストール

```bash
pip install -r requirements.txt
```

---

### 6. Gemini APIキーの取得

1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. 「APIキーを作成」をクリック
4. 表示されたキー（`AIza...` で始まる文字列）をコピー

---

### 7. .envファイルの作成

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

`.env` を開き、取得したAPIキーとプロジェクトフォルダのパスを設定します。

```env
GEMINI_API_KEY=取得したAPIキーを貼り付ける
AGENT_DIR=プロジェクトフォルダの絶対パス
```

> `.env` は `.gitignore` により、リポジトリにコミットされません。

---

### 8. 動作確認

```bash
python main.py --morning
```

以下のように応答が返れば成功です。

```
🌅 おはようございます！朝のTo-Doセッションです
```

---

## 常駐起動（スケジューラー）として運用する場合

[SCHEDULER_SETUP.md](./SCHEDULER_SETUP.md) を参照してください。

---

## コマンド一覧

| コマンド | 内容 |
|---|---|
| `python main.py --morning` | 朝セッションを今すぐ実行 |
| `python main.py --evening` | 夜セッションを今すぐ実行 |
| `python main.py` | スケジューラーとして常駐起動 |
