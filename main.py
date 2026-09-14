"""Начальный сценарий проекта «Система рекомендаций городских маршрутов»."""

from datetime import date

from entities import (
    create_user,
    print_user,
    create_route,
    print_route,
    create_recommendation,
    print_recommendation,
)


def main():
    print("=== Система рекомендаций городских маршрутов ===")
    print(f"Дата: {date.today()}")
    print()

    # 1. Пользователь
    user, msg = create_user("Артур", "Москва", "архитектура")
    print(msg)
    print_user(user)
    print()

    # 2. Маршрут
    route, msg = create_route("Исторический центр", "архитектура", 4.5, 6)
    print(msg)
    print_route(route)
    print()

    # 3. Рекомендация
    recommendation, msg = create_recommendation(user, route)
    print(msg)
    print_recommendation(recommendation)


if __name__ == "__main__":
    main()