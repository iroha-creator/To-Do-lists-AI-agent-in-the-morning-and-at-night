"""Gemini APIを使った対話エージェントモジュール"""

import os
import re
import google.generativeai as genai
import todo_manager as tm


def _build_system_prompt(session: str, existing_todos: list) -> str:
    session_label = "朝" if session == "morning" else "夜"
    existing_str = tm.format_todo_list(existing_todos)
    return f"""あなたはユーザーの{session_label}のTo-Do管理を手伝うアシスタントです。

【役割】
- ユーザーと自然な会話をしながらTo-Doリストを一緒に作成・確認する
- ユーザーの言葉からタスクを的確に読み取る
- 曖昧な場合は具体的な質問で明確にする
- 励ましの言葉を添えて前向きにサポートする

【今日の既存タスク】
{existing_str}

【出力ルール】
- タスクを確定したいときは必ず末尾に以下のJSON形式で出力する:
  TASKS_JSON: ["タスク1", "タスク2", ...]
- 完了確認をするときは末尾に以下のJSON形式で出力する:
  DONE_IDS_JSON: [1, 3, ...]  ← 完了したタスクのIDリスト
- 会話中は自然な日本語で話しかける
"""


def _extract_json_field(text: str, field: str):
    pattern = rf"{field}:\s*(\[.*?\])"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        import json
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def _clean_response(text: str) -> str:
    """JSONタグ行を除いた会話部分を返す"""
    text = re.sub(r"TASKS_JSON:.*", "", text, flags=re.DOTALL)
    text = re.sub(r"DONE_IDS_JSON:.*", "", text, flags=re.DOTALL)
    return text.strip()


class TodoAgent:
    def __init__(self, session: str, todo_file: str):
        self.session = session
        self.todo_file = todo_file
        self.history: list[dict] = []

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=_build_system_prompt(
                session, tm.get_today_todos(todo_file)
            ),
        )
        self.chat = self.model.start_chat(history=[])

    def _send(self, user_input: str) -> str:
        response = self.chat.send_message(user_input)
        return response.text

    def run_morning_session(self):
        """朝セッション: タスク作成フロー"""
        print("\n" + "=" * 50)
        print("🌅 おはようございます！朝のTo-Doセッションです")
        print("=" * 50)

        # 既存タスクの表示
        existing = tm.get_today_todos(self.todo_file)
        if existing:
            print("\n📋 今日の既存タスク:")
            print(tm.format_todo_list(existing))

        # 開始メッセージ
        opening = self._send("朝のセッションを開始します。ユーザーに今日のタスクを確認してください。")
        print(f"\n🤖 {_clean_response(opening)}\n")

        # 対話ループ
        while True:
            user_input = input("あなた: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "終了", "おわり"):
                print("セッションを終了します。")
                break

            response = self._send(user_input)
            clean = _clean_response(response)

            # タスク抽出
            tasks = _extract_json_field(response, "TASKS_JSON")
            if tasks:
                added = tm.add_todos(self.todo_file, tasks, self.session)
                print(f"\n🤖 {clean}")
                print("\n✅ 以下のタスクを追加しました:")
                print(tm.format_todo_list(added))

                cont = input("\n他に追加しますか？(はい/いいえ): ").strip()
                if cont in ("いいえ", "no", "n", "終わり", "なし"):
                    print("\n今日も頑張りましょう！またの夜に！\n")
                    break
            else:
                print(f"\n🤖 {clean}\n")

    def run_evening_session(self):
        """夜セッション: 完了確認フロー"""
        print("\n" + "=" * 50)
        print("🌙 おつかれさまです！夜のTo-Doセッションです")
        print("=" * 50)

        todos = tm.get_today_todos(self.todo_file)
        if not todos:
            print("\n今日のタスクはありませんでした。ゆっくり休んでください！\n")
            return

        print("\n📋 今日のタスク一覧:")
        print(tm.format_todo_list(todos))

        # 開始メッセージ
        opening = self._send(
            f"夜のセッションです。今日のタスクは以下の通りです:\n{tm.format_todo_list(todos)}\n"
            "ユーザーに完了したタスクを確認してください。"
        )
        print(f"\n🤖 {_clean_response(opening)}\n")

        # 対話ループ
        while True:
            user_input = input("あなた: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "終了", "おわり"):
                print("セッションを終了します。")
                break

            response = self._send(user_input)
            clean = _clean_response(response)

            # 完了ID抽出
            done_ids = _extract_json_field(response, "DONE_IDS_JSON")
            if done_ids:
                for todo_id in done_ids:
                    tm.update_todo_status(self.todo_file, todo_id, done=True)
                updated = tm.get_today_todos(self.todo_file)
                print(f"\n🤖 {clean}")
                print("\n📋 更新後のタスク:")
                print(tm.format_todo_list(updated))

                cont = input("\n他に更新しますか？(はい/いいえ): ").strip()
                if cont in ("いいえ", "no", "n"):
                    done_count = sum(1 for t in updated if t["done"])
                    total = len(updated)
                    print(f"\n今日は {done_count}/{total} タスク完了！ゆっくり休んでください 🌙\n")
                    break
            else:
                print(f"\n🤖 {clean}\n")
