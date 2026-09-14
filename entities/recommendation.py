"""Сущность «Рекомендация»."""

from entities.interest import check_interest

    
def create_recommendation(user_name, user_interest, route_name, route_interest):
    """Формирование рекомендации маршрута для пользователя.

    Возвращает кортеж (route_name_out, score, text, message) из простых
    типов, без использования коллекций.
    """
    if user_name is None or route_name is None:
        return None, None, None, "Ошибка: пользователь или маршрут не заданы"

    if check_interest(user_interest, route_interest):
        score = 1.0
        text = f"Рекомендуем маршрут «{route_name}» для пользователя {user_name}."
    else:
        score = 0.0
        text = f"Маршрут «{route_name}» не соответствует интересу «{user_interest}»."

    return route_name, score, text, "Рекомендация сформирована"


def print_recommendation(route_name, score, text):
    """Вывод рекомендации."""
    if route_name is None:
        print("Рекомендация не сформирована.")
        return
    print(text)
    print(f"Коэффициент соответствия: {score}")