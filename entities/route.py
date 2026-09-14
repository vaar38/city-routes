"""Сущность «Маршрут»."""


def create_route(name, interest, length_km, points_count):
    """Создание маршрута с проверкой данных."""
    if not name:
        return None, "Ошибка: название маршрута не указано"
    if length_km <= 0:
        return None, "Ошибка: протяжённость должна быть больше нуля"
    if points_count < 2:
        return None, "Ошибка: в маршруте должно быть минимум 2 точки"

    route = {
        "name": name,
        "interest": interest,
        "length_km": length_km,
        "points_count": points_count,
    }
    return route, "Маршрут успешно создан"


def print_route(route):
    """Вывод информации о маршруте."""
    if route is None:
        print("Маршрут не создан.")
        return
    print(f"Маршрут: {route['name']}")
    print(f"Тематика: {route['interest']}")
    print(f"Протяжённость: {route['length_km']} км")
    print(f"Количество точек: {route['points_count']}")