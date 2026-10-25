"""Точка запуска: консольное меню «Системы рекомендаций городских маршрутов»."""

from recommendations import (
    create_recommendation,
    dismiss_recommendation,
    get_recommendation_status,
    is_route_recommended,
    recommend_routes,
    show_recommendations,
)
from routes import (
    add_route,
    delete_route,
    filter_routes_by_interest,
    filter_routes_by_length,
    find_route,
    find_route_by_id,
    show_routes,
    sort_routes,
)
from storage import (
    load_recommendations,
    load_routes,
    load_users,
    save_recommendations,
    save_routes,
    save_users,
)
from users import add_user, change_interest, find_user_by_id, show_users
from utils import input_float, input_int, input_text

MENU = """
=== Система рекомендаций городских маршрутов ===
-- Маршруты --
1. Показать маршруты (по длине)
2. Найти маршрут по названию
3. Отобрать маршруты по длине и тематике
4. Добавить маршрут
5. Удалить маршрут
-- Профиль --
6. Показать пользователей
7. Добавить пользователя
8. Изменить интерес пользователя
-- Рекомендации --
9. Подобрать маршруты для пользователя
10. Рекомендовать маршрут пользователю
11. Отклонить рекомендацию
12. Показать рекомендации
0. Выход"""


def search_routes(routes: list[dict]) -> None:
    """Сценарий «Поиск маршрута по названию»."""
    show_routes(find_route(routes, input_text("Часть названия: ")))


def filter_routes(routes: list[dict]) -> None:
    """Сценарий «Фильтрация маршрутов по длине и тематике»."""
    max_km = input_float("Максимальная длина, км: ")
    interest = input("Тематика (Enter — любая): ").strip()
    result = list(filter_routes_by_length(routes, max_km))
    if interest:
        result = filter_routes_by_interest(result, interest)
    show_routes(result)


def create_new_route(routes: list[dict]) -> None:
    """Сценарий «Добавление маршрута»."""
    try:
        route = add_route(
            routes,
            input_text("Название: "),
            input_text("Тематика: "),
            input_float("Длина, км: "),
            input_int("Количество точек: "),
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Маршрут добавлен, ID = {route['id']}")


def remove_route(routes: list[dict]) -> None:
    """Сценарий «Удаление маршрута»."""
    if delete_route(routes, input_int("ID маршрута: ")):
        print("Маршрут удалён.")
    else:
        print("Маршрут не найден.")


def create_new_user(users: list[dict]) -> None:
    """Сценарий «Добавление пользователя»."""
    try:
        user = add_user(
            users,
            input_text("Имя: "),
            input_text("E-mail: "),
            input_text("Интерес: "),
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Пользователь добавлен, ID = {user['id']}")


def edit_interest(users: list[dict]) -> None:
    """Сценарий «Изменение интереса пользователя»."""
    user_id = input_int("ID пользователя: ")
    if change_interest(users, user_id, input_text("Новый интерес: ")):
        print("Интерес изменён.")
    else:
        print("Пользователь не найден.")


def pick_routes(routes: list[dict], users: list[dict]) -> None:
    """Сценарий «Подбор маршрутов под интерес пользователя»."""
    user = find_user_by_id(users, input_int("ID пользователя: "))
    if user is None:
        print("Пользователь не найден.")
        return
    print(f"Интерес: {user['interest']}")
    show_routes(recommend_routes(routes, user))


def create_new_recommendation(
    recommendations: list[dict],
    routes: list[dict],
    users: list[dict],
) -> None:
    """Сценарий «Рекомендовать маршрут пользователю»."""
    route = find_route_by_id(routes, input_int("ID маршрута: "))
    if route is None:
        print("Маршрут не найден.")
        return
    user = find_user_by_id(users, input_int("ID пользователя: "))
    if user is None:
        print("Пользователь не найден.")
        return

    print(get_recommendation_status(
        is_route_recommended(recommendations, route["id"], user["id"])
    ))
    rec = create_recommendation(recommendations, route, user)
    if rec is None:
        print("Рекомендация не создана: интересы не совпадают или она уже активна.")
    else:
        print(f"Рекомендация создана, ID = {rec['id']}")


def reject_recommendation(recommendations: list[dict]) -> None:
    """Сценарий «Отклонить рекомендацию»."""
    if dismiss_recommendation(recommendations, input_int("ID рекомендации: ")):
        print("Рекомендация отклонена.")
    else:
        print("Активная рекомендация с таким ID не найдена.")


def main() -> None:
    """Загрузить данные, запустить цикл меню, сохранить данные при выходе."""
    routes = load_routes()
    users = load_users()
    recommendations = load_recommendations()

    try:
        while True:
            print(MENU)
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                show_routes(sort_routes(routes))
            elif choice == "2":
                search_routes(routes)
            elif choice == "3":
                filter_routes(routes)
            elif choice == "4":
                create_new_route(routes)
            elif choice == "5":
                remove_route(routes)
            elif choice == "6":
                show_users(users)
            elif choice == "7":
                create_new_user(users)
            elif choice == "8":
                edit_interest(users)
            elif choice == "9":
                pick_routes(routes, users)
            elif choice == "10":
                create_new_recommendation(recommendations, routes, users)
            elif choice == "11":
                reject_recommendation(recommendations)
            elif choice == "12":
                show_recommendations(recommendations, routes, users)
            elif choice == "0":
                break
            else:
                print("Нет такого пункта меню.")
    except (KeyboardInterrupt, EOFError):
        print("\nРабота прервана.")
    finally:
        save_routes(routes)
        save_users(users)
        save_recommendations(recommendations)
        print("Данные сохранены.")


if __name__ == "__main__":
    main()
