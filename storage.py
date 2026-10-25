"""Загрузка и сохранение данных в JSON-файлах."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
ROUTES_FILE = DATA_DIR / "routes.json"
USERS_FILE = DATA_DIR / "users.json"
RECOMMENDATIONS_FILE = DATA_DIR / "recommendations.json"


def load_json(filename: Path) -> list[dict]:
    """Прочитать список словарей из JSON-файла.

    При отсутствии файла или некорректном JSON вернуть пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename.name} не найден, начинаем с пустого списка.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename.name} повреждён, начинаем с пустого списка.")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename.name} имеет неверный формат.")
        return []
    return data


def save_json(filename: Path, items: list[dict]) -> None:
    """Записать список словарей в JSON-файл."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=4)


def load_routes(filename: Path = ROUTES_FILE) -> list[dict]:
    """Загрузить маршруты."""
    return load_json(filename)


def save_routes(routes: list[dict], filename: Path = ROUTES_FILE) -> None:
    """Сохранить маршруты."""
    save_json(filename, routes)


def load_users(filename: Path = USERS_FILE) -> list[dict]:
    """Загрузить пользователей."""
    return load_json(filename)


def save_users(users: list[dict], filename: Path = USERS_FILE) -> None:
    """Сохранить пользователей."""
    save_json(filename, users)


def load_recommendations(filename: Path = RECOMMENDATIONS_FILE) -> list[dict]:
    """Загрузить рекомендации."""
    return load_json(filename)


def save_recommendations(
    recommendations: list[dict],
    filename: Path = RECOMMENDATIONS_FILE,
) -> None:
    """Сохранить рекомендации."""
    save_json(filename, recommendations)
