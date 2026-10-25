"""Тесты слоя SQLite: схема, импорт из JSON, параметризованные запросы."""

import sqlite3

import pytest

from db.database import fetch_all, fetch_one, get_connection
from db.import_json import main as import_json
from storage import save_json


@pytest.fixture
def db_path(tmp_path):
    """Временная база, заполненная из маленьких JSON-файлов."""
    save_json(tmp_path / "routes.json", [
        {"id": 1, "name": "Центр", "interest": "архитектура", "length_km": 4.5, "points_count": 6},
        {"id": 2, "name": "Парки", "interest": "парки", "length_km": 3.0, "points_count": 4},
    ])
    save_json(tmp_path / "users.json", [
        {"id": 1, "name": "Артур", "email": "a@example.com", "interest": "архитектура"},
    ])
    save_json(tmp_path / "recs.json", [
        {"id": 1, "route_id": 1, "user_id": 1, "score": 0.9, "is_dismissed": False},
        {"id": 2, "route_id": 1, "user_id": 1, "score": 0.5, "is_dismissed": True},
    ])
    path = tmp_path / "test.sqlite"
    import_json(path, tmp_path / "routes.json", tmp_path / "users.json", tmp_path / "recs.json")
    return path


def test_import_counts(db_path):
    counts = {
        "SELECT COUNT(*) AS n FROM interests": 2,
        "SELECT COUNT(*) AS n FROM users": 1,
        "SELECT COUNT(*) AS n FROM routes": 2,
        "SELECT COUNT(*) AS n FROM recommendations": 2,
    }
    for sql, expected in counts.items():
        assert fetch_one(sql, db_path=db_path)["n"] == expected


def test_import_is_repeatable(db_path, tmp_path):
    import_json(db_path, tmp_path / "routes.json", tmp_path / "users.json", tmp_path / "recs.json")
    assert fetch_one("SELECT COUNT(*) AS n FROM routes", db_path=db_path)["n"] == 2


def test_bool_converted_to_int(db_path):
    rows = fetch_all("SELECT is_dismissed FROM recommendations ORDER BY id", db_path=db_path)
    assert [row["is_dismissed"] for row in rows] == [0, 1]


def test_foreign_keys_enforced(db_path):
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO recommendations (route_id, user_id) VALUES (999, 1)")
    conn.close()


def test_join_returns_names(db_path):
    row = fetch_one(
        """
        SELECT users.name AS user_name, routes.name AS route_name
        FROM recommendations
        JOIN users ON recommendations.user_id = users.id
        JOIN routes ON recommendations.route_id = routes.id
        WHERE recommendations.id = ?
        """,
        (1,),
        db_path=db_path,
    )
    assert row["user_name"] == "Артур"
    assert row["route_name"] == "Центр"


def test_parameter_is_not_sql(db_path):
    """Попытка SQL-инъекции через параметр — просто строка, совпадений нет."""
    rows = fetch_all(
        "SELECT id FROM routes WHERE name = ?",
        ("x' OR '1'='1",),
        db_path=db_path,
    )
    assert rows == []
