"""Класс Route и функции работы с коллекцией маршрутов."""

from typing import Iterator


class Route:
    """Тематический маршрут по городу."""

    def __init__(
        self,
        route_id: int,
        name: str,
        interest: str,
        length_km: float,
        points_count: int,
    ) -> None:
        """Создать маршрут. Проверки перенесены из add_route() ПР2."""
        if not name.strip():
            raise ValueError("Название маршрута не указано")
        if not Route.validate_length(length_km):
            raise ValueError("Протяжённость должна быть больше нуля")
        if points_count < 2:
            raise ValueError("В маршруте должно быть минимум 2 точки")
        self.id = route_id
        self.name = name.strip()
        self.interest = interest.strip().lower()
        self.length_km = length_km
        self.points_count = points_count

    @staticmethod
    def validate_length(length_km: float) -> bool:
        """Проверить, что протяжённость положительная."""
        return length_km > 0

    @classmethod
    def from_data(cls, data: dict) -> "Route":
        """Создать маршрут из словаря, прочитанного из JSON."""
        return cls(
            data["id"],
            data["name"],
            data["interest"],
            data["length_km"],
            data["points_count"],
        )

    def is_suitable_for(self, max_length_km: float) -> bool:
        """Проверить, что маршрут не длиннее max_length_km километров."""
        return self.length_km <= max_length_km

    def has_interest(self, interest: str) -> bool:
        """Проверить, относится ли маршрут к тематике interest."""
        return self.interest == interest.strip().lower()

    @property
    def info(self) -> str:
        """Краткое описание маршрута для вывода."""
        return f"{self.length_km} км, {self.points_count} точек"

    def __str__(self) -> str:
        return f"{self.name} ({self.interest}), {self.info}"


def next_id(items: list) -> int:
    """Вернуть следующий свободный идентификатор для списка объектов."""
    return max((item.id for item in items), default=0) + 1


def add_route(
    routes: list[Route],
    name: str,
    interest: str,
    length_km: float,
    points_count: int,
) -> Route:
    """Создать объект Route и добавить его в коллекцию."""
    route = Route(next_id(routes), name, interest, length_km, points_count)
    routes.append(route)
    return route


def delete_route(routes: list[Route], route_id: int) -> bool:
    """Удалить маршрут по идентификатору. Вернуть True, если удалён."""
    for index, route in enumerate(routes):
        if route.id == route_id:
            del routes[index]
            return True
    return False


def find_route_by_id(routes: list[Route], route_id: int) -> Route | None:
    """Найти маршрут по идентификатору."""
    for route in routes:
        if route.id == route_id:
            return route
    return None


def find_route(routes: list[Route], query: str) -> list[Route]:
    """Найти маршруты, в названии которых встречается подстрока query."""
    query = query.strip().lower()
    return [route for route in routes if query in route.name.lower()]


def check_route_length(routes: list[Route], route_id: int, max_length_km: float) -> bool:
    """Найти маршрут и проверить его длину методом Route.is_suitable_for()."""
    route = find_route_by_id(routes, route_id)
    if route is None:
        return False
    return route.is_suitable_for(max_length_km)


def filter_routes_by_length(routes: list[Route], max_length_km: float) -> Iterator[Route]:
    """Отобрать маршруты не длиннее max_length_km (генератор)."""
    for route in routes:
        if route.is_suitable_for(max_length_km):
            yield route


def filter_routes_by_interest(routes: list[Route], interest: str) -> list[Route]:
    """Отобрать маршруты с заданной тематикой."""
    return [route for route in routes if route.has_interest(interest)]


def sort_routes(routes: list[Route], reverse: bool = False) -> list[Route]:
    """Вернуть маршруты, отсортированные по протяжённости."""
    return sorted(routes, key=lambda route: route.length_km, reverse=reverse)


def show_routes(routes: list[Route]) -> None:
    """Вывести список маршрутов таблицей."""
    if not routes:
        print("Маршрутов нет.")
        return
    print(f"{'ID':>3}  {'Название':<28} {'Тематика':<14} {'Км':>5} {'Точек':>5}")
    for route in routes:
        print(
            f"{route.id:>3}  {route.name:<28} {route.interest:<14} "
            f"{route.length_km:>5} {route.points_count:>5}"
        )
