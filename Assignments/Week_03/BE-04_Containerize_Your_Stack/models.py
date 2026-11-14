from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime | None = None