"""Перенос данных проекта из JSON-файлов в SQLite.

Запуск из корня проекта: python -m db.import_json

Порядок импорта важен из-за внешних ключей: сначала interests,
затем users и routes (ссылаются на interests), последними
recommendations (ссылаются на users и routes). Перед вставкой таблицы
очищаются в обратном порядке, поэтому скрипт можно запускать повторно.
"""

import sqlite3
from pathlib import Path

from db.database import DB_PATH, create_schema, get_connection
from storage import RECOMMENDATIONS_FILE, ROUTES_FILE, USERS_FILE, load_json


def import_interests(conn: sqlite3.Connection, routes: list[dict], users: list[dict]) -> dict:
    """Собрать тематики из маршрутов и интересов пользователей.

    В JSON интерес хранится строкой, в БД — отдельной таблицей.
    Вернуть словарь «название → id» для подстановки внешних ключей.
    """
    names = sorted({item["interest"].strip().lower() for item in routes + users})
    rows = [(index, name) for index, name in enumerate(names, start=1)]
    conn.executemany("INSERT INTO interests (id, name) VALUES (?, ?)", rows)
    return {name: interest_id for interest_id, name in rows}


def import_users(conn: sqlite3.Connection, users: list[dict], interest_ids: dict) -> None:
    conn.executemany(
        """
        INSERT INTO users (id, name, email, interest_id)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                user["id"],
                user["name"],
                user["email"],
                interest_ids[user["interest"].strip().lower()],
            )
            for user in users
        ],
    )


def import_routes(conn: sqlite3.Connection, routes: list[dict], interest_ids: dict) -> None:
    conn.executemany(
        """
        INSERT INTO routes (id, name, interest_id, length_km, points_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                route["id"],
                route["name"],
                interest_ids[route["interest"].strip().lower()],
                route["length_km"],
                route["points_count"],
            )
            for route in routes
        ],
    )


def import_recommendations(conn: sqlite3.Connection, recommendations: list[dict]) -> None:
    conn.executemany(
        """
        INSERT INTO recommendations (id, route_id, user_id, score, is_dismissed)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                rec["id"],
                rec["route_id"],
                rec["user_id"],
                rec.get("score", 1.0),
                int(rec.get("is_dismissed", False)),  # bool из JSON → 0/1
            )
            for rec in recommendations
        ],
    )


def clear_tables(conn: sqlite3.Connection) -> None:
    """Очистить таблицы в порядке, обратном зависимостям."""
    conn.execute("DELETE FROM recommendations")
    conn.execute("DELETE FROM routes")
    conn.execute("DELETE FROM users")
    conn.execute("DELETE FROM interests")


def main(
    db_path: Path = DB_PATH,
    routes_file: Path = ROUTES_FILE,
    users_file: Path = USERS_FILE,
    recommendations_file: Path = RECOMMENDATIONS_FILE,
) -> None:
    routes = load_json(routes_file)
    users = load_json(users_file)
    recommendations = load_json(recommendations_file)

    conn = get_connection(db_path)
    try:
        create_schema(conn)
        clear_tables(conn)
        interest_ids = import_interests(conn, routes, users)
        import_users(conn, users, interest_ids)
        import_routes(conn, routes, interest_ids)
        import_recommendations(conn, recommendations)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(
        f"Импортировано: интересов {len(interest_ids)}, пользователей {len(users)}, "
        f"маршрутов {len(routes)}, рекомендаций {len(recommendations)}"
    )


if __name__ == "__main__":
    main()
