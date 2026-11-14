import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


def get_connection():
    """Create a connection to PostgreSQL."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def initialize_database():
    """Execute the SQL initialization script."""
    sql_file = Path(__file__).parent / "sql" / "init.sql"
    sql_script = sql_file.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.execute(sql_script)