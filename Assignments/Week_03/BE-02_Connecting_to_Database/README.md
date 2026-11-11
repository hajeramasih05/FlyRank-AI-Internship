# TaskFlow API – Database Integration

A RESTful task management API built using Python, FastAPI and SQLite. This project demonstrates backend development with persistent database storage and CRUD operations.

**Developer:** Hajera Masih

## Technology Stack

- Python 3.11
- FastAPI
- Uvicorn
- SQLite
- SQL

## Features

- Create new tasks.
- Retrieve all tasks.
- Retrieve individual tasks by ID.
- Update task titles and completion status.
- Delete existing tasks.
- Store task records permanently using SQLite.
- Automatically initialize the database and sample records.

## Project Structure

```text
BE-02_Connecting_to_Database/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── tasks.db (generated automatically)
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate to the project

```bash
cd Assignments/Week_03/BE-02_Connecting_to_Database
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the application

```bash
python -m uvicorn main:app --reload
```

The API will run at:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Database Structure

**Database:** SQLite

**Table:** tasks

| Column | Data Type | Description |
|---|---|---|
| id | INTEGER | Primary key, auto-increment |
| title | TEXT | Task description |
| done | INTEGER | Completion status (0 or 1) |

## SQL Operations Practiced

- SELECT – Retrieve records.
- INSERT – Add records.
- UPDATE – Modify records.
- DELETE – Remove records.
- WHERE – Filter records.
- COUNT – Count database records.

## API Documentation

FastAPI provides interactive API documentation through Swagger UI:

`http://127.0.0.1:8000/docs`

## Database Persistence

Unlike the previous in-memory implementation, this version stores task records in an SQLite database file.

The database is initialized automatically when the application starts. Existing records are preserved across server restarts.