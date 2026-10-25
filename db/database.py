"""Подключение Python к базе данных SQLite."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "city_routes.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение и включить проверку внешних ключей.

    По умолчанию SQLite не проверяет FOREIGN KEY, поэтому
    PRAGMA выполняется при каждом подключении.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Выполнить sql/schema.sql (несколько команд одной операцией)."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def fetch_all(sql: str, params: tuple = (), db_path: Path = DB_PATH) -> list[sqlite3.Row]:
    """Выполнить SELECT и вернуть все строки.

    row_factory = sqlite3.Row даёт доступ к полям по имени:
    row["name"] в Python и {{ row.name }} в шаблоне.
    Значения передаются только через параметры ?, не через f-строки.
    """
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def fetch_one(sql: str, params: tuple = (), db_path: Path = DB_PATH) -> sqlite3.Row | None:
    """Выполнить SELECT и вернуть первую строку или None."""
    rows = fetch_all(sql, params, db_path)
    return rows[0] if rows else None
