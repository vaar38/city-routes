"""Сущность «Интерес»."""


def check_interest(user_interest, route_interest):
    """Проверка совпадения интереса пользователя с тематикой маршрута."""
    if not user_interest or not route_interest:
        return False
    return user_interest.strip().lower() == route_interest.strip().lower()