"""Страницы маршрутов: данные берутся из SQLite SQL-запросами (ПР7).

Номера запросов соответствуют sql/queries.sql.
"""

from django.shortcuts import render

from db.database import fetch_all, fetch_one

SHORT_WALK_KM = 5

# Запрос 1
ROUTES_SQL = """
    SELECT
        routes.id,
        routes.name,
        interests.name AS interest,
        routes.length_km,
        routes.points_count
    FROM routes
    JOIN interests ON routes.interest_id = interests.id
    ORDER BY routes.name
"""

# Запрос 3
INTERESTS_SQL = """
    SELECT id, name
    FROM interests
    ORDER BY name
"""

# Запрос 5: пустая тематика или пустая длина означают «без ограничения»
SEARCH_SQL = """
    SELECT
        routes.id,
        routes.name,
        interests.name AS interest,
        routes.length_km,
        routes.points_count
    FROM routes
    JOIN interests ON routes.interest_id = interests.id
    WHERE (? = '' OR interests.name = ?)
      AND (? IS NULL OR routes.length_km <= ?)
    ORDER BY routes.length_km
"""

# Запрос 6
ROUTE_SQL = """
    SELECT
        routes.id,
        routes.name,
        interests.name AS interest,
        routes.length_km,
        routes.points_count,
        routes.description
    FROM routes
    JOIN interests ON routes.interest_id = interests.id
    WHERE routes.id = ?
"""

# Запрос 7
ROUTE_USERS_SQL = """
    SELECT
        users.name AS user_name,
        recommendations.score
    FROM recommendations
    JOIN users ON recommendations.user_id = users.id
    WHERE recommendations.route_id = ?
      AND recommendations.is_dismissed = 0
    ORDER BY recommendations.score DESC
"""


def routes(request):
    context = {
        "routes": fetch_all(ROUTES_SQL),
    }
    return render(request, "routes/route_list.html", context)


def route_detail(request, route_id):
    route = fetch_one(ROUTE_SQL, (route_id,))
    context = {
        "route": route,
        "is_short": route is not None and route["length_km"] <= SHORT_WALK_KM,
        "users": fetch_all(ROUTE_USERS_SQL, (route_id,)) if route else [],
    }
    return render(
        request,
        "routes/route_detail.html",
        context,
        status=404 if route is None else 200,
    )


def search(request):
    interest = request.GET.get("interest", "").strip().lower()
    max_km_text = request.GET.get("max_km", "").strip().replace(",", ".")
    submitted = "interest" in request.GET or "max_km" in request.GET

    error = None
    max_km = None
    if max_km_text:
        try:
            max_km = float(max_km_text)
        except ValueError:
            error = "Длина должна быть числом, например 4.5"

    found = []
    if submitted and error is None:
        found = fetch_all(SEARCH_SQL, (interest, interest, max_km, max_km))

    context = {
        "interests": fetch_all(INTERESTS_SQL),
        "interest": interest,
        "max_km": max_km_text,
        "submitted": submitted,
        "error": error,
        "routes": found,
    }
    return render(request, "routes/search.html", context)
