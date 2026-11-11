from fastapi import FastAPI, HTTPException
from database import get_connection, initialize_database
from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class TaskCreate(BaseModel):
    title: str | None = None

app = FastAPI(
    title="TaskFlow API",
    description="""
    A RESTful task management API built with Python, FastAPI and SQLite.

    Developed by Hajera Masih.

    This API provides endpoints to create, retrieve, update,
    and delete tasks with permanent database storage.
    """,
    version="2.0.0"
)

# Initialize database when the application starts
initialize_database()


@app.get("/", tags=["General"])
def home():
    return {
        "project": "TaskFlow API",
        "tagline": "Organize. Track. Accomplish.",
        "developer": "Hajera Masih",
        "version": "2.0.0",
        "message": "Welcome to TaskFlow API!"
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "service": "TaskFlow API",
        "developer": "Hajera Masih"
    }


# Retrieve all tasks from SQLite
@app.get("/tasks", tags=["Tasks"])
def get_tasks():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks")

        tasks = cursor.fetchall()

        return [
            {
                "id": task["id"],
                "title": task["title"],
                "done": bool(task["done"])
            }
            for task in tasks
        ]

    finally:
        connection.close()


# Retrieve a specific task by ID
@app.get("/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: int):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        task = cursor.fetchone()

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return {
            "id": task["id"],
            "title": task["title"],
            "done": bool(task["done"])
        }

    finally:
        connection.close()

# Create a new task in SQLite
@app.post("/tasks", status_code=201, tags=["Tasks"])
def create_task(task_data: TaskCreate):

    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (task_data.title.strip(), 0)
        )

        connection.commit()

        new_task_id = cursor.lastrowid

        return {
            "id": new_task_id,
            "title": task_data.title.strip(),
            "done": False
        }

    finally:
        connection.close()

# Update an existing task
@app.put("/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, task_data: TaskUpdate):

    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    if task_data.title is not None and not task_data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )

        existing_task = cursor.fetchone()

        if existing_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        new_title = (
            task_data.title.strip()
            if task_data.title is not None
            else existing_task["title"]
        )

        new_done = (
            int(task_data.done)
            if task_data.done is not None
            else existing_task["done"]
        )

        cursor.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (new_title, new_done, task_id)
        )

        connection.commit()

        return {
            "id": task_id,
            "title": new_title,
            "done": bool(new_done)
        }

    finally:
        connection.close()

# Delete an existing task
@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        connection.commit()

        return {
            "message": "Task deleted successfully"
        }

    finally:
        connection.close()