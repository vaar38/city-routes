"""Сущность «Пользователь»."""


def create_user(name, city, interest):
    """Создание пользователя и проверка корректности данных."""
    if not name:
        return None, "Ошибка: имя пользователя не указано"
    if not city:
        return None, "Ошибка: город не указан"
    if not interest:
        return None, "Ошибка: интерес не указан"

    user = {
        "name": name,
        "city": city,
        "interest": interest,
    }
    return user, "Пользователь успешно создан"


def print_user(user):
    """Вывод информации о пользователе."""
    if user is None:
        print("Пользователь не создан.")
        return
    print(f"Пользователь: {user['name']}")
    print(f"Город: {user['city']}")
    print(f"Интерес: {user['interest']}")