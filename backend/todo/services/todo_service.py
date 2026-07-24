import sqlite3
from typing import Optional, List
from todo.models.todo_model import Todo
from todo.db.database import get_connection

class TodoService:
    def list_all(self) -> List[Todo]:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM todos ORDER BY created_at DESC").fetchall()
            return [Todo.from_row(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
            return Todo.from_row(row) if row else None
        finally:
            conn.close()

    def create(self, title: str, description: str = "") -> Todo:
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO todos (title, description) VALUES (?, ?)",
                (title, description)
            )
            conn.commit()
            todo = Todo(id=cursor.lastrowid, title=title, description=description)
            return todo
        finally:
            conn.close()

    def update(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Todo]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
            if not row:
                return None
            existing = Todo.from_row(row)
            new_title = title if title is not None else existing.title
            new_desc = description if description is not None else existing.description
            new_completed = completed if completed is not None else existing.completed
            conn.execute(
                "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                (new_title, new_desc, 1 if new_completed else 0, todo_id)
            )
            conn.commit()
            return self.get_by_id(todo_id)
        finally:
            conn.close()

    def delete(self, todo_id: int) -> bool:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
            if not row:
                return False
            conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            return True
        finally:
            conn.close()
