import sqlite3
from typing import Optional, List
from datetime import datetime
from todo.models.todo_model import Todo
from todo.db.database import get_connection

class TodoService:
    def list_all(self, search: str = "", status: str = "", priority: str = "", page: int = 1, per_page: int = 10) -> dict:
        conn = get_connection()
        try:
            query = "SELECT * FROM todos WHERE 1=1"
            params = []
            if search:
                query += " AND (title LIKE ? OR description LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])
            if status == "completed":
                query += " AND completed = 1"
            elif status == "active":
                query += " AND completed = 0"
            if priority:
                query += " AND priority = ?"
                params.append(priority)
            count_row = conn.execute(f"SELECT COUNT(*) FROM ({query})", params).fetchone()
            total = count_row[0]
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([per_page, (page - 1) * per_page])
            rows = conn.execute(query, params).fetchall()
            return {
                "todos": [Todo.from_row(row) for row in rows],
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": max(1, (total + per_page - 1) // per_page)
            }
        finally:
            conn.close()

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
            return Todo.from_row(row) if row else None
        finally:
            conn.close()

    def create(self, title: str, description: str = "", priority: str = "medium", due_date: Optional[str] = None) -> Todo:
        conn = get_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO todos (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
                (title, description, priority, due_date)
            )
            conn.commit()
            todo = Todo(id=cursor.lastrowid, title=title, description=description, priority=priority, due_date=due_date)
            return todo
        finally:
            conn.close()

    def update(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None, priority: Optional[str] = None, due_date: Optional[str] = None) -> Optional[Todo]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
            if not row:
                return None
            existing = Todo.from_row(row)
            new_title = title if title is not None else existing.title
            new_desc = description if description is not None else existing.description
            new_completed = completed if completed is not None else existing.completed
            new_priority = priority if priority is not None else existing.priority
            new_due_date = due_date if due_date is not None else existing.due_date
            conn.execute(
                "UPDATE todos SET title = ?, description = ?, completed = ?, priority = ?, due_date = ?, updated_at = ? WHERE id = ?",
                (new_title, new_desc, 1 if new_completed else 0, new_priority, new_due_date, datetime.now().isoformat(), todo_id)
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

    def clear_completed(self) -> int:
        conn = get_connection()
        try:
            cursor = conn.execute("DELETE FROM todos WHERE completed = 1")
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
