"""To-Doデータの読み書きを管理するモジュール"""

import json
import os
from datetime import date
from typing import TypedDict


class TodoItem(TypedDict):
    id: int
    task: str
    done: bool
    session: str  # "morning" or "evening"
    date: str


def load_todos(filepath: str) -> list[TodoItem]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(filepath: str, todos: list[TodoItem]) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def get_today_todos(filepath: str) -> list[TodoItem]:
    todos = load_todos(filepath)
    today = str(date.today())
    return [t for t in todos if t["date"] == today]


def add_todos(filepath: str, tasks: list[str], session: str) -> list[TodoItem]:
    todos = load_todos(filepath)
    today = str(date.today())
    next_id = max((t["id"] for t in todos), default=0) + 1

    new_items: list[TodoItem] = []
    for i, task in enumerate(tasks):
        item: TodoItem = {
            "id": next_id + i,
            "task": task,
            "done": False,
            "session": session,
            "date": today,
        }
        new_items.append(item)

    todos.extend(new_items)
    save_todos(filepath, todos)
    return new_items


def update_todo_status(filepath: str, todo_id: int, done: bool) -> bool:
    todos = load_todos(filepath)
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = done
            save_todos(filepath, todos)
            return True
    return False


def format_todo_list(todos: list[TodoItem]) -> str:
    if not todos:
        return "（タスクなし）"
    lines = []
    for t in todos:
        mark = "✅" if t["done"] else "⬜"
        lines.append(f"  {mark} [{t['id']}] {t['task']}")
    return "\n".join(lines)
