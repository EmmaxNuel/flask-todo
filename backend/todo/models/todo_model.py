from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Todo:
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    id: Optional[int] = None
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row.get("description", ""),
            completed=bool(row["completed"]),
            priority=row.get("priority", "medium"),
            due_date=row.get("due_date"),
            created_at=row["created_at"],
            updated_at=row.get("updated_at", "")
        )
