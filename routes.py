"""Функции работы с маршрутами.

Маршрут хранится словарём:
{"id": 1, "name": "...", "interest": "...", "length_km": 4.5, "points_count": 6}
"""

from typing import Iterator


def next_id(items: list[dict]) -> int:
    """Вернуть следующий свободный идентификатор для списка словарей."""
    return max((item["id"] for item in items), default=0) + 1


def add_route(
    routes: list[dict],
    name: str,
    interest: str,
    length_km: float,
    points_count: int,
) -> dict:
    """Создать маршрут и добавить его в список routes.

    Проверки перенесены из create_route() ПР1: при некорректных данных
    выбрасывается ValueError.
    """
    if not name.strip():
        raise ValueError("Название маршрута не указано")
    if length_km <= 0:
        raise ValueError("Протяжённость должна быть больше нуля")
    if points_count < 2:
        raise ValueError("В маршруте должно быть минимум 2 точки")

    route = {
        "id": next_id(routes),
        "name": name.strip(),
        "interest": interest.strip().lower(),
        "length_km": length_km,
        "points_count": points_count,
    }
    routes.append(route)
    return route


def delete_route(routes: list[dict], route_id: int) -> bool:
    """Удалить маршрут по идентификатору. Вернуть True, если удалён."""
    for index, route in enumerate(routes):
        if route["id"] == route_id:
            del routes[index]
            return True
    return False


def find_route_by_id(routes: list[dict], route_id: int) -> dict | None:
    """Найти маршрут по идентификатору."""
    for route in routes:
        if route["id"] == route_id:
            return route
    return None


def find_route(routes: list[dict], query: str) -> list[dict]:
    """Найти маршруты, в названии которых встречается подстрока query."""
    query = query.strip().lower()
    return [route for route in routes if query in route["name"].lower()]


def check_route_length(routes: list[dict], route_id: int, max_length_km: float) -> bool:
    """Проверить, что маршрут не длиннее max_length_km километров."""
    route = find_route_by_id(routes, route_id)
    if route is None:
        return False
    return route["length_km"] <= max_length_km


def filter_routes_by_length(routes: list[dict], max_length_km: float) -> Iterator[dict]:
    """Отобрать маршруты не длиннее max_length_km (генератор)."""
    for route in routes:
        if route["length_km"] <= max_length_km:
            yield route


def filter_routes_by_interest(routes: list[dict], interest: str) -> list[dict]:
    """Отобрать маршруты с заданной тематикой."""
    interest = interest.strip().lower()
    return [route for route in routes if route["interest"] == interest]


def sort_routes(routes: list[dict], reverse: bool = False) -> list[dict]:
    """Вернуть маршруты, отсортированные по протяжённости."""
    return sorted(routes, key=lambda route: route["length_km"], reverse=reverse)


def show_routes(routes: list[dict]) -> None:
    """Вывести список маршрутов таблицей."""
    if not routes:
        print("Маршрутов нет.")
        return
    print(f"{'ID':>3}  {'Название':<28} {'Тематика':<14} {'Км':>5} {'Точек':>5}")
    for route in routes:
        print(
            f"{route['id']:>3}  {route['name']:<28} {route['interest']:<14} "
            f"{route['length_km']:>5} {route['points_count']:>5}"
        )
