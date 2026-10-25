from django.shortcuts import render

from db.database import fetch_one


def index(request):
    """Главная: краткая сводка из SQLite (агрегатные запросы 11 и 12)."""
    context = {
        "routes_count": fetch_one("SELECT COUNT(*) AS n FROM routes")["n"],
        "active_count": fetch_one(
            "SELECT COUNT(*) AS n FROM recommendations WHERE is_dismissed = 0"
        )["n"],
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    return render(request, "homepage/404.html", status=404)
