"""Страницы рекомендаций, подбора и статистики: SQL-запросы к SQLite (ПР7).

Номера запросов соответствуют sql/queries.sql.
"""

from django.shortcuts import render

from db.database import fetch_all, fetch_one

# Запрос 8
ACTIVE_SQL = """
    SELECT
        recommendations.id,
        users.name AS user_name,
        routes.id AS route_id,
        routes.name AS route_name,
        routes.length_km,
        recommendations.score
    FROM recommendations
    JOIN users ON recommendations.user_id = users.id
    JOIN routes ON recommendations.route_id = routes.id
    WHERE recommendations.is_dismissed = 0
    ORDER BY users.name, recommendations.score DESC
"""

# Запрос 9
DETAIL_SQL = """
    SELECT
        recommendations.id,
        recommendations.score,
        recommendations.is_dismissed,
        users.name AS user_name,
        users.email,
        routes.id AS route_id,
        routes.name AS route_name,
        routes.length_km,
        interests.name AS interest
    FROM recommendations
    JOIN users ON recommendations.user_id = users.id
    JOIN routes ON recommendations.route_id = routes.id
    JOIN interests ON routes.interest_id = interests.id
    WHERE recommendations.id = ?
"""

# Запрос 2
USERS_SQL = """
    SELECT id, name, email
    FROM users
    ORDER BY name
"""

USER_SQL = """
    SELECT users.id, users.name, interests.name AS interest
    FROM users
    JOIN interests ON users.interest_id = interests.id
    WHERE users.id = ?
"""

# Запрос 10
PICK_SQL = """
    SELECT
        routes.id,
        routes.name,
        routes.length_km
    FROM routes
    JOIN users ON users.interest_id = routes.interest_id
    WHERE users.id = ?
      AND routes.id NOT IN (
          SELECT route_id
          FROM recommendations
          WHERE user_id = ?
            AND is_dismissed = 0
      )
    ORDER BY routes.length_km
"""

# Запрос 11
SUMMARY_SQL = """
    SELECT
        COUNT(*) AS routes_count,
        ROUND(AVG(length_km), 1) AS avg_length,
        MIN(length_km) AS min_length,
        MAX(length_km) AS max_length,
        SUM(points_count) AS points_total
    FROM routes
"""

# Запрос 12
ACTIVE_COUNT_SQL = """
    SELECT COUNT(*) AS active_count
    FROM recommendations
    WHERE is_dismissed = 0
"""

# Запрос 13
BY_INTEREST_SQL = """
    SELECT
        interests.name AS interest,
        COUNT(routes.id) AS routes_count,
        ROUND(AVG(routes.length_km), 1) AS avg_length
    FROM interests
    LEFT JOIN routes ON routes.interest_id = interests.id
    GROUP BY interests.id, interests.name
    ORDER BY routes_count DESC, interest
"""

# Запрос 14
BY_ROUTE_SQL = """
    SELECT
        routes.id,
        routes.name AS route_name,
        COUNT(recommendations.id) AS recs_count,
        ROUND(AVG(recommendations.score), 2) AS avg_score
    FROM routes
    LEFT JOIN recommendations
        ON recommendations.route_id = routes.id
       AND recommendations.is_dismissed = 0
    GROUP BY routes.id, routes.name
    ORDER BY recs_count DESC, route_name
"""

# Запрос 15
BY_USER_SQL = """
    SELECT
        users.name AS user_name,
        COUNT(recommendations.id) AS total,
        SUM(recommendations.is_dismissed) AS dismissed
    FROM users
    LEFT JOIN recommendations ON recommendations.user_id = users.id
    GROUP BY users.id, users.name
    ORDER BY total DESC, user_name
"""

# Запрос 16: порог задаёт пользователь, передаётся параметром
POPULAR_SQL = """
    SELECT
        routes.id,
        routes.name AS route_name,
        COUNT(recommendations.id) AS recs_count
    FROM routes
    JOIN recommendations ON recommendations.route_id = routes.id
    WHERE recommendations.is_dismissed = 0
    GROUP BY routes.id, routes.name
    HAVING COUNT(recommendations.id) > ?
    ORDER BY recs_count DESC
"""

# Запрос 17
TOP_SQL = """
    SELECT
        routes.name AS route_name,
        COUNT(recommendations.id) AS recs_count
    FROM routes
    JOIN recommendations ON recommendations.route_id = routes.id
    WHERE recommendations.is_dismissed = 0
    GROUP BY routes.id, routes.name
    ORDER BY recs_count DESC, route_name
    LIMIT 3
"""


def recommendations(request):
    context = {
        "recommendations": fetch_all(ACTIVE_SQL),
    }
    return render(request, "recommendations/recommendation_list.html", context)


def recommendation_detail(request, rec_id):
    rec = fetch_one(DETAIL_SQL, (rec_id,))
    return render(
        request,
        "recommendations/recommendation_detail.html",
        {"rec": rec},
        status=404 if rec is None else 200,
    )


def pick(request):
    user = None
    routes = []
    user_id = request.GET.get("user", "")
    if user_id.isdigit():
        user = fetch_one(USER_SQL, (int(user_id),))
        if user is not None:
            routes = fetch_all(PICK_SQL, (user["id"], user["id"]))
    context = {
        "users": fetch_all(USERS_SQL),
        "selected": user_id,
        "user": user,
        "routes": routes,
    }
    return render(request, "recommendations/pick.html", context)


def statistics(request):
    min_text = request.GET.get("min", "1")
    min_count = int(min_text) if min_text.isdigit() else 1
    context = {
        "summary": fetch_one(SUMMARY_SQL),
        "active_count": fetch_one(ACTIVE_COUNT_SQL)["active_count"],
        "by_interest": fetch_all(BY_INTEREST_SQL),
        "by_route": fetch_all(BY_ROUTE_SQL),
        "by_user": fetch_all(BY_USER_SQL),
        "min_count": min_count,
        "popular": fetch_all(POPULAR_SQL, (min_count,)),
        "top": fetch_all(TOP_SQL),
    }
    return render(request, "recommendations/statistics.html", context)
