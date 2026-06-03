"""To-Doエージェント エントリーポイント

使い方:
  python main.py              # スケジューラー起動（朝・夜の自動実行）
  python main.py --morning    # 朝セッションを今すぐ実行
  python main.py --evening    # 夜セッションを今すぐ実行
"""

import argparse
import os
import sys
from dotenv import load_dotenv


def check_env():
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ エラー: GEMINI_API_KEY が設定されていません。")
        print("   .env.example を参考に .env ファイルを作成してください。")
        sys.exit(1)


def main():
    load_dotenv()
    check_env()

    parser = argparse.ArgumentParser(description="朝・夜のTo-Doエージェント")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--morning", action="store_true", help="朝セッションを今すぐ実行")
    group.add_argument("--evening", action="store_true", help="夜セッションを今すぐ実行")
    args = parser.parse_args()

    todo_file = os.environ.get("TODO_FILE", "todos.json")

    if args.morning:
        from agent import TodoAgent
        TodoAgent(session="morning", todo_file=todo_file).run_morning_session()
    elif args.evening:
        from agent import TodoAgent
        TodoAgent(session="evening", todo_file=todo_file).run_evening_session()
    else:
        from scheduler import start_scheduler
        start_scheduler()


if __name__ == "__main__":
    main()
