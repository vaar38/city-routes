"""Сущность «Рекомендация»."""

from entities.interest import check_interest


def create_recommendation(user, route):
    """Формирование рекомендации маршрута для пользователя."""
    if user is None or route is None:
        return None, "Ошибка: пользователь или маршрут не заданы"

    if check_interest(user["interest"], route["interest"]):
        score = 1.0
        text = (
            f"Рекомендуем маршрут «{route['name']}» "
            f"для пользователя {user['name']}."
        )
    else:
        score = 0.0
        text = (
            f"Маршрут «{route['name']}» не соответствует "
            f"интересу «{user['interest']}»."
        )

    recommendation = {
        "user": user["name"],
        "route": route["name"],
        "score": score,
        "text": text,
    }
    return recommendation, "Рекомендация сформирована"


def print_recommendation(recommendation):
    """Вывод рекомендации."""
    if recommendation is None:
        print("Рекомендация не сформирована.")
        return
    print(recommendation["text"])
    print(f"Коэффициент соответствия: {recommendation['score']}")