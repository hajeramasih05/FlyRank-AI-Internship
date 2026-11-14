from repository import TaskRepository
from models import Task


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all_tasks(self) -> list[Task]:
        return self.repository.get_all()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def create_task(
        self, title: str, description: str | None, completed: bool
    ) -> Task:
        return self.repository.create(title, description, completed)

    def update_task(self, task_id: int, updates: dict) -> Task | None:
        return self.repository.update(task_id, updates)

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)