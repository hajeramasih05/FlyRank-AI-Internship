
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from database import get_connection, initialize_database
from repository import PostgresTaskRepository
from service import TaskService
from schemas import TaskCreate, TaskUpdate, TaskResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="BE-04 Containerized Task API",
    description="FastAPI application connected to PostgreSQL using Docker.",
    version="1.0.0",
    lifespan=lifespan,
)

repository = PostgresTaskRepository()
task_service = TaskService(repository)


@app.get("/")
def home():
    return {"message": "BE-04 Task API is running"}


@app.get("/health")
def health():
    try:
        with get_connection() as connection:
            connection.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = task_service.get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
    return task_service.create_task(
        task.title,
        task.description,
        task.completed,
    )


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    updated_task = task_service.update_task(
        task_id,
        task.model_dump(exclude_unset=True),
    )

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
