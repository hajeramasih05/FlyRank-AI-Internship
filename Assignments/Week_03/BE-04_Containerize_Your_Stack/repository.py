
from datetime import datetime
from typing import Protocol

from models import Task
from database import get_connection

class TaskRepository(Protocol):
    """Interface that every task repository must implement."""

    def get_all(self) -> list[Task]:
        ...

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def create(
        self, title: str, description: str | None, completed: bool
    ) -> Task:
        ...

    def update(self, task_id: int, updates: dict) -> Task | None:
        ...

    def delete(self, task_id: int) -> bool:
        ...


class InMemoryTaskRepository:
    """Stores tasks temporarily in Python memory."""

    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_id = 1

    def get_all(self) -> list[Task]:
        return list(self.tasks.values())

    def get_by_id(self, task_id: int) -> Task | None:
        return self.tasks.get(task_id)

    def create(
        self, title: str, description: str | None, completed: bool
    ) -> Task:
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=completed,
            created_at=datetime.now(),
        )

        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def update(self, task_id: int, updates: dict) -> Task | None:
        task = self.tasks.get(task_id)

        if task is None:
            return None

        for field, value in updates.items():
            setattr(task, field, value)

        return task

    def delete(self, task_id: int) -> bool:
        return self.tasks.pop(task_id, None) is not None




class PostgresTaskRepository:
    """Stores and retrieves tasks using PostgreSQL."""

    def get_all(self) -> list[Task]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY id"
            ).fetchall()

        return [Task(**row) for row in rows]

    def get_by_id(self, task_id: int) -> Task | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = %s",
                (task_id,)
            ).fetchone()

        return Task(**row) if row else None

    def create(
        self, title: str, description: str | None, completed: bool
    ) -> Task:
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO tasks (title, description, completed)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (title, description, completed)
            ).fetchone()

        return Task(**row)

    def update(self, task_id: int, updates: dict) -> Task | None:
        allowed_fields = {"title", "description", "completed"}
        updates = {
            key: value for key, value in updates.items()
            if key in allowed_fields
        }

        if not updates:
            return self.get_by_id(task_id)

        set_clause = ", ".join(
            f"{field} = %s" for field in updates
        )
        values = list(updates.values()) + [task_id]

        with get_connection() as connection:
            row = connection.execute(
                f"""
                UPDATE tasks
                SET {set_clause}
                WHERE id = %s
                RETURNING *
                """,
                values
            ).fetchone()

        return Task(**row) if row else None

    def delete(self, task_id: int) -> bool:
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,)
            )

        return cursor.rowcount > 0