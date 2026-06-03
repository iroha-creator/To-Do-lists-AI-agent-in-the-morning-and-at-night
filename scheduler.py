"""朝・夜のセッションをスケジュール実行するモジュール"""

import os
import time
import schedule
from agent import TodoAgent


def _run_session(session: str):
    todo_file = os.environ.get("TODO_FILE", "todos.json")
    agent = TodoAgent(session=session, todo_file=todo_file)
    if session == "morning":
        agent.run_morning_session()
    else:
        agent.run_evening_session()


def start_scheduler():
    morning_hour = int(os.environ.get("MORNING_HOUR", 8))
    morning_min = int(os.environ.get("MORNING_MINUTE", 0))
    evening_hour = int(os.environ.get("EVENING_HOUR", 21))
    evening_min = int(os.environ.get("EVENING_MINUTE", 0))

    morning_time = f"{morning_hour:02d}:{morning_min:02d}"
    evening_time = f"{evening_hour:02d}:{evening_min:02d}"

    schedule.every().day.at(morning_time).do(_run_session, session="morning")
    schedule.every().day.at(evening_time).do(_run_session, session="evening")

    print(f"📅 スケジューラー起動")
    print(f"   朝セッション: {morning_time}")
    print(f"   夜セッション: {evening_time}")
    print("   終了するには Ctrl+C を押してください\n")

    while True:
        schedule.run_pending()
        time.sleep(30)
