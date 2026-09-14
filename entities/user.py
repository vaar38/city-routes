"""Сущность «Пользователь»."""


def create_user(name, city, interest):
    """Создание пользователя и проверка корректности данных.

    Возвращает кортеж (name, city, interest, message) из простых типов,
    без использования коллекций (dict/list), т.к. на ПР1 работа
    со сложными структурами данных ещё не изучалась.
    """
    if not name:
        return None, None, None, "Ошибка: имя пользователя не указано"
    if not city:
        return None, None, None, "Ошибка: город не указан"
    if not interest:
        return None, None, None, "Ошибка: интерес не указан"

    return name, city, interest, "Пользователь успешно создан"


def print_user(name, city, interest):
    """Вывод информации о пользователе."""
    if name is None:
        print("Пользователь не создан.")
        return
    print(f"Пользователь: {name}")
    print(f"Город: {city}")
    print(f"Интерес: {interest}")