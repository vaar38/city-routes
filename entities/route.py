"""Сущность «Маршрут»."""


def create_route(name, interest, length_km, points_count):
    """Создание маршрута с проверкой данных.

    Возвращает кортеж (name, interest, length_km, points_count, message)
    из простых типов, без использования коллекций.
    """
    if not name:
        return None, None, None, None, "Ошибка: название маршрута не указано"
    if length_km <= 0:
        return None, None, None, None, "Ошибка: протяжённость должна быть больше нуля"
    if points_count < 2:
        return None, None, None, None, "Ошибка: в маршруте должно быть минимум 2 точки"

    return name, interest, length_km, points_count, "Маршрут успешно создан"


def print_route(name, interest, length_km, points_count):
    """Вывод информации о маршруте."""
    if name is None:
        print("Маршрут не создан.")
        return
    print(f"Маршрут: {name}")
    print(f"Тематика: {interest}")
    print(f"Протяжённость: {length_km} км")
    print(f"Количество точек: {points_count}")