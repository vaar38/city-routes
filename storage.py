"""Загрузка и сохранение данных в JSON-файлах.

JSON хранит простые данные, приложение работает с объектами:
при загрузке словари превращаются в Route / User / Recommendation,
при сохранении — обратно в словари. Рекомендация в JSON хранит
route_id и user_id, при загрузке они заменяются ссылками на объекты.
"""

import json
from pathlib import Path

from models import Recommendation, Route, User
from models.routes import find_route_by_id
from models.users import find_user_by_id

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


def load_routes(filename: Path = ROUTES_FILE) -> list[Route]:
    """Загрузить маршруты: JSON → объекты Route (некорректные записи пропускаются)."""
    routes = []
    for data in load_json(filename):
        try:
            routes.append(Route.from_data(data))
        except (KeyError, ValueError) as error:
            print(f"Пропущен маршрут {data}: {error}")
    return routes


def save_routes(routes: list[Route], filename: Path = ROUTES_FILE) -> None:
    """Сохранить маршруты: объекты Route → JSON."""
    save_json(filename, [
        {
            "id": route.id,
            "name": route.name,
            "interest": route.interest,
            "length_km": route.length_km,
            "points_count": route.points_count,
        }
        for route in routes
    ])


def load_users(filename: Path = USERS_FILE) -> list[User]:
    """Загрузить пользователей: JSON → объекты User."""
    users = []
    for data in load_json(filename):
        try:
            users.append(User.from_data(data))
        except (KeyError, ValueError) as error:
            print(f"Пропущен пользователь {data}: {error}")
    return users


def save_users(users: list[User], filename: Path = USERS_FILE) -> None:
    """Сохранить пользователей: объекты User → JSON."""
    save_json(filename, [
        {"id": user.id, "name": user.name, "email": user.email, "interest": user.interest}
        for user in users
    ])


def load_recommendations(
    routes: list[Route],
    users: list[User],
    filename: Path = RECOMMENDATIONS_FILE,
) -> list[Recommendation]:
    """Загрузить рекомендации и восстановить связи с объектами Route и User.

    Запись, ссылающаяся на несуществующий маршрут или пользователя, пропускается.
    """
    recommendations = []
    for data in load_json(filename):
        route = find_route_by_id(routes, data.get("route_id"))
        user = find_user_by_id(users, data.get("user_id"))
        if route is None or user is None:
            print(f"Пропущена рекомендация {data.get('id')}: нет маршрута или пользователя")
            continue
        recommendations.append(Recommendation(
            data["id"],
            route,
            user,
            data.get("score", 1.0),
            data.get("is_dismissed", False),
        ))
    return recommendations


def save_recommendations(
    recommendations: list[Recommendation],
    filename: Path = RECOMMENDATIONS_FILE,
) -> None:
    """Сохранить рекомендации: ссылки на объекты → route_id / user_id."""
    save_json(filename, [
        {
            "id": rec.id,
            "route_id": rec.route.id,
            "user_id": rec.user.id,
            "score": rec.score,
            "is_dismissed": rec.is_dismissed,
        }
        for rec in recommendations
    ])
