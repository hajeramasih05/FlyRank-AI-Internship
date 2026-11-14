# BE-04: Containerize Your Stack

**Track:** Backend AI Engineering  
**Week:** 3  
**Assignment:** BE-04 — Containerize Your Stack

## 1. Project Overview

This project containerizes a FastAPI task management application using Docker and PostgreSQL.

The application uses a layered backend architecture with a repository pattern, allowing database operations to remain separate from API routes and business logic.

Docker Compose runs the FastAPI application and PostgreSQL database together.

## 2. Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- PostgreSQL 18.7
- Psycopg
- Docker
- Docker Compose
- Python-dotenv
- SQL

## 3. Project Structure

```text
BE-04_Containerize_Your_Stack/
│
├── sql/
│   └── init.sql
│
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── database.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── models.py
├── repository.py
├── requirements.txt
├── schemas.py
├── service.py
└── README.md
```

## 4. Architecture

The application follows a layered architecture:

```text
Client
  |
  v
FastAPI Routes (main.py)
  |
  v
Service Layer (service.py)
  |
  v
Repository Layer (repository.py)
  |
  v
Database Connection (database.py)
  |
  v
PostgreSQL
```

### Repository Pattern

Two repository implementations are provided:

- `InMemoryTaskRepository`: stores tasks temporarily in Python memory.
- `PostgresTaskRepository`: stores tasks permanently in PostgreSQL.

Both implement the same repository interface.

The application uses `PostgresTaskRepository`. Switching storage implementations does not require changing the service layer or API routes.

## 5. Database Configuration

Database credentials are stored in `.env`.

The `.env` file is excluded from Git using `.gitignore`.

A `.env.example` template is provided for configuration reference.

The database table is defined in `sql/init.sql`.

## 6. Docker Configuration

### Dockerfile

The Dockerfile builds the FastAPI application image using Python 3.11 slim.

It installs dependencies, copies the application files and starts Uvicorn.

### Docker Compose

Docker Compose defines two services:

- `db`: PostgreSQL 18.7 database.
- `app`: FastAPI application.

The application waits for the database health check before starting.

A named Docker volume, `be04_postgres_data`, stores PostgreSQL data outside the container.

## 7. Running the Application

### Prerequisites

- Docker Desktop
- Docker Compose

### Step 1: Configure environment

Copy `.env.example` to `.env` and configure your local database credentials.

### Step 2: Start the stack

```bash
docker compose up --build
```

To run in detached mode:

```bash
docker compose up -d --build
```

### Step 3: Check container status

```bash
docker compose ps
```

### Step 4: Access the API

API:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

Health check:

http://localhost:8000/health

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Database health check |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a specific task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## 9. Data Persistence Verification

PostgreSQL data is stored in the named Docker volume `be04_postgres_data`.

Persistence can be verified using the following procedure:

1. Create a task through the API.
2. Retrieve the task and confirm it exists.
3. Stop and remove the containers using:

```bash
docker compose down
```

4. Recreate the application and database:

```bash
docker compose up -d --build
```

5. Retrieve the tasks again and verify that the previously created record remains available.

The named volume is reused when the containers are recreated.

**Important:** `docker compose down -v` must not be used during this test because it removes the named volume.

## 10. Conclusion

This assignment demonstrates containerization of a FastAPI application, PostgreSQL integration, environment-based configuration, layered backend architecture, repository pattern implementation and persistent database storage using Docker volumes.

Docker Compose simplifies deployment by allowing the application and database to run together through a single command.