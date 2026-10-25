from django.shortcuts import render

from models.recommendations import find_recommendation_by_id
from storage import load_recommendations, load_routes, load_users


def load_all():
    """Загрузить маршруты, пользователей и рекомендации со связями."""
    return load_recommendations(load_routes(), load_users())


def recommendations(request):
    context = {
        "recommendations": load_all(),
    }
    return render(request, "recommendations/recommendation_list.html", context)


def recommendation_detail(request, rec_id):
    rec = find_recommendation_by_id(load_all(), rec_id)
    context = {
        "rec": rec,
    }
    return render(
        request,
        "recommendations/recommendation_detail.html",
        context,
        status=404 if rec is None else 200,
    )
