"""Функции работы с рекомендациями.

Рекомендация связывает пользователя и маршрут:
{"id": 1, "route_id": 1, "user_id": 1, "score": 1.0, "is_dismissed": false}

Правило: у пользователя не может быть двух активных рекомендаций одного
и того же маршрута. Отклонённая рекомендация не мешает создать новую.
"""


def check_interest(user_interest: str, route_interest: str) -> bool:
    """Проверить совпадение интереса пользователя с тематикой маршрута (из ПР1)."""
    if not user_interest or not route_interest:
        return False
    return user_interest.strip().lower() == route_interest.strip().lower()


def recommend_routes(routes: list[dict], user: dict) -> list[dict]:
    """Подобрать маршруты, тематика которых совпадает с интересом пользователя."""
    return [route for route in routes if check_interest(user["interest"], route["interest"])]


def is_route_recommended(recommendations: list[dict], route_id: int, user_id: int) -> bool:
    """Проверить, есть ли у пользователя активная рекомендация этого маршрута."""
    for rec in recommendations:
        if (
            rec["route_id"] == route_id
            and rec["user_id"] == user_id
            and not rec["is_dismissed"]
        ):
            return True
    return False


def create_recommendation(
    recommendations: list[dict],
    route: dict,
    user: dict,
) -> dict | None:
    """Создать рекомендацию маршрута для пользователя.

    Вернуть None, если интересы не совпадают или такая рекомендация
    уже активна.
    """
    if not check_interest(user["interest"], route["interest"]):
        return None
    if is_route_recommended(recommendations, route["id"], user["id"]):
        return None

    rec = {
        "id": max((r["id"] for r in recommendations), default=0) + 1,
        "route_id": route["id"],
        "user_id": user["id"],
        "score": 1.0,
        "is_dismissed": False,
    }
    recommendations.append(rec)
    return rec


def dismiss_recommendation(recommendations: list[dict], rec_id: int) -> bool:
    """Отклонить рекомендацию: запись остаётся, меняется признак is_dismissed."""
    for rec in recommendations:
        if rec["id"] == rec_id and not rec["is_dismissed"]:
            rec["is_dismissed"] = True
            return True
    return False


def get_recommendation_status(is_recommended: bool) -> str:
    """Вернуть текстовый статус рекомендации."""
    if is_recommended:
        return "Маршрут уже рекомендован пользователю"
    return "Маршрут ещё не рекомендован пользователю"


def show_recommendations(
    recommendations: list[dict],
    routes: list[dict],
    users: list[dict],
) -> None:
    """Вывести рекомендации с названиями маршрутов и именами пользователей."""
    if not recommendations:
        print("Рекомендаций нет.")
        return
    route_names = {route["id"]: route["name"] for route in routes}
    user_names = {user["id"]: user["name"] for user in users}
    for rec in recommendations:
        status = "отклонена" if rec["is_dismissed"] else "активна"
        print(
            f"{rec['id']:>3}  {user_names.get(rec['user_id'], '?'):<20} → "
            f"{route_names.get(rec['route_id'], '?'):<28} [{status}]"
        )
