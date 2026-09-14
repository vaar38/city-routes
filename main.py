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
    user_name, user_city, user_interest, msg = create_user(
        "Артур", "Москва", "архитектура"
    )
    print(msg)
    print_user(user_name, user_city, user_interest)
    print()

    # 2. Маршрут
    route_name, route_interest, route_length, route_points, msg = create_route(
        "Исторический центр", "архитектура", 4.5, 6
    )
    print(msg)
    print_route(route_name, route_interest, route_length, route_points)
    print()

    # 3. Рекомендация
    rec_route, rec_score, rec_text, msg = create_recommendation(
        user_name, user_interest, route_name, route_interest
    )
    print(msg)
    print_recommendation(rec_route, rec_score, rec_text)


if __name__ == "__main__":
    main()