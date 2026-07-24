from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Todo:
    title: str
    description: str = ""
    completed: bool = False
    id: Optional[int] = None
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row.get("description", ""),
            completed=bool(row["completed"]),
            created_at=row["created_at"]
        )
