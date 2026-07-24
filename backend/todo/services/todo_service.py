import sqlite3
from typing import Optional, List
from todo.models.todo_model import Todo
from todo.db.database import get_connection

class TodoService:
    def __init__(self):
        self.db = get_connection()

    def list_all(self) -> List[Todo]:
        rows = self.db.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()
        return [Todo.from_row(row) for row in rows]

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        row = self.db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        return Todo.from_row(row) if row else None

    def create(self, title: str, description: str = "") -> Todo:
        cursor = self.db.execute(
            "INSERT INTO todos (title, description) VALUES (?, ?)",
            (title, description)
        )
        self.db.commit()
        todo = Todo(id=cursor.lastrowid, title=title, description=description)
        return todo

    def update(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        existing = self.get_by_id(todo_id)
        if not existing:
            return None
        new_title = title if title is not None else existing.title
        new_desc = description if description is not None else existing.description
        new_completed = completed if completed is not None else existing.completed
        self.db.execute(
            "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
            (new_title, new_desc, 1 if new_completed else 0, todo_id)
        )
        self.db.commit()
        return self.get_by_id(todo_id)

    def delete(self, todo_id: int) -> bool:
        existing = self.get_by_id(todo_id)
        if not existing:
            return False
        self.db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self.db.commit()
        return True
