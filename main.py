from datetime import date


def register_user(name, city, interest):
    """Регистрация пользователя и вывод его данных."""
    if not name:
        return "Ошибка: имя пользователя не указано"
    if not city:
        return "Ошибка: город не указан"
    if not interest:
        return "Ошибка: интерес не указан"

    return (
        f"Пользователь {name} зарегистрирован.\n"
        f"Город: {city}\n"
        f"Интерес: {interest}"
    )


def match_interest(user_interest, route_interest):
    """Сравнение интереса пользователя с тематикой маршрута."""
    if user_interest.lower() == route_interest.lower():
        return True
    return False


def recommend_route(user_interest, route_name, route_interest, route_length):
    """Формирование рекомендации маршрута для пользователя."""
    if match_interest(user_interest, route_interest):
        return (
            f"Рекомендуем маршрут: {route_name}\n"
            f"Тематика: {route_interest}\n"
            f"Протяжённость: {route_length} км\n"
            f"Маршрут соответствует вашему интересу «{user_interest}»."
        )
    return (
        f"Маршрут «{route_name}» не соответствует вашему интересу "
        f"«{user_interest}»."
    )


# --- Начальный сценарий ---
user_name = "Артур"
user_city = "Москва"
user_interest = "архитектура"

route_name = "Исторический центр"
route_interest = "архитектура"
route_length = 4.5

today = date.today()

print("=== Система рекомендаций городских маршрутов ===")
print(f"Дата: {today}")
print()
print(register_user(user_name, user_city, user_interest))
print()
print(recommend_route(user_interest, route_name, route_interest, route_length))