
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None    

app = FastAPI(
    title="TaskFlow API",
    description="""
    A RESTful task management API built with Python and FastAPI.

    Developed by Hajera Masih.

    This API provides endpoints to create, retrieve, update,
    and delete tasks through standard HTTP methods.
    """,
    version="1.0.0"
)


@app.get("/", tags=["General"])
def home():
    return {
        "project": "TaskFlow API",
        "tagline": "Organize. Track. Accomplish.",
        "developer": "Hajera Masih",
        "version": "1.0.0",
        "message": "Welcome to TaskFlow API!"
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "service": "TaskFlow API",
        "developer": "Hajera Masih"
    }

# Sample tasks stored in memory
tasks = [
    {
        "id": 1,
        "title": "Complete Python assignment",
        "done": False
    },
    {
        "id": 2,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 3,
        "title": "Update GitHub profile",
        "done": True
    }
]


# Retrieve all tasks
@app.get("/tasks", tags=["Tasks"])
def get_tasks():
    return tasks


# Retrieve a specific task by ID
@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.post("/tasks", status_code=201, tags=["Tasks"])
def create_task(task_data: TaskCreate):

    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": new_id,
        "title": task_data.title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, task_data: TaskUpdate):

    for task in tasks:
        if task["id"] == task_id:

            if task_data.title is not None:
                if not task_data.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Task title cannot be empty"
                    )

                task["title"] = task_data.title.strip()

            if task_data.done is not None:
                task["done"] = task_data.done

            if task_data.title is None and task_data.done is None:
                raise HTTPException(
                    status_code=400,
                    detail="Provide at least one field to update"
                )

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return {
                "message": "Task deleted successfully",
                "deleted_task": task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )