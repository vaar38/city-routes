"""Класс Recommendation и функции работы с рекомендациями.

Рекомендация связывает объекты User и Route (композиция).
Правило: у пользователя не может быть двух активных рекомендаций одного
и того же маршрута. Отклонённая рекомендация не мешает создать новую.
"""

from .routes import Route, next_id
from .users import User


class Recommendation:
    """Маршрут, предложенный пользователю."""

    def __init__(
        self,
        rec_id: int,
        route: Route,
        user: User,
        score: float = 1.0,
        is_dismissed: bool = False,
    ) -> None:
        self.id = rec_id
        self.route = route
        self.user = user
        self.score = score
        self.is_dismissed = is_dismissed

    def dismiss(self) -> None:
        """Отклонить рекомендацию: объект остаётся в коллекции."""
        self.is_dismissed = True

    @property
    def is_active(self) -> bool:
        """Рекомендация активна, пока её не отклонили."""
        return not self.is_dismissed

    def __str__(self) -> str:
        status = "отклонена" if self.is_dismissed else "активна"
        return f"{self.user.name} → {self.route.name} [{status}]"


def check_interest(user_interest: str, route_interest: str) -> bool:
    """Проверить совпадение интереса пользователя с тематикой маршрута (из ПР1)."""
    if not user_interest or not route_interest:
        return False
    return user_interest.strip().lower() == route_interest.strip().lower()


def recommend_routes(routes: list[Route], user: User) -> list[Route]:
    """Подобрать маршруты, тематика которых совпадает с интересом пользователя."""
    return [route for route in routes if check_interest(user.interest, route.interest)]


def is_route_recommended(
    recommendations: list[Recommendation],
    route: Route,
    user: User,
) -> bool:
    """Проверить, есть ли у пользователя активная рекомендация этого маршрута."""
    return any(
        rec.route.id == route.id and rec.user.id == user.id and rec.is_active
        for rec in recommendations
    )


def create_recommendation(
    recommendations: list[Recommendation],
    route: Route,
    user: User,
) -> Recommendation | None:
    """Создать рекомендацию и добавить её в коллекцию.

    Вернуть None, если интересы не совпадают или такая рекомендация уже активна.
    """
    if not check_interest(user.interest, route.interest):
        return None
    if is_route_recommended(recommendations, route, user):
        return None
    rec = Recommendation(next_id(recommendations), route, user)
    recommendations.append(rec)
    return rec


def dismiss_recommendation(recommendations: list[Recommendation], rec_id: int) -> bool:
    """Найти активную рекомендацию и вызвать её метод dismiss()."""
    for rec in recommendations:
        if rec.id == rec_id and rec.is_active:
            rec.dismiss()
            return True
    return False


def get_recommendation_status(is_recommended: bool) -> str:
    """Вернуть текстовый статус рекомендации."""
    if is_recommended:
        return "Маршрут уже рекомендован пользователю"
    return "Маршрут ещё не рекомендован пользователю"


def show_recommendations(recommendations: list[Recommendation]) -> None:
    """Вывести рекомендации: имена и названия берутся из связанных объектов."""
    if not recommendations:
        print("Рекомендаций нет.")
        return
    for rec in recommendations:
        print(f"{rec.id:>3}  {rec}")
