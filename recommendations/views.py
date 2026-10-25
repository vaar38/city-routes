from django.http import HttpResponse

from homepage.views import page
from models.recommendations import find_recommendation_by_id
from storage import load_recommendations, load_routes, load_users


def load_all():
    """Загрузить маршруты, пользователей и рекомендации со связями."""
    return load_recommendations(load_routes(), load_users())


def recommendations(request):
    items = ""
    for rec in load_all():
        status = "активна" if rec.is_active else "отклонена"
        badge = "bg-success" if rec.is_active else "bg-secondary"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/recommendations/{rec.id}/">{rec.user.name} → {rec.route.name}</a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Рекомендации</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("City Routes – рекомендации", content))


def recommendation_detail(request, rec_id):
    rec = find_recommendation_by_id(load_all(), rec_id)
    if rec is None:
        content = """
        <h1 class="text-danger">Рекомендация не найдена</h1>
        <a href="/recommendations/" class="btn btn-outline-secondary">
            ← к списку рекомендаций
        </a>
        """
        return HttpResponse(page("Рекомендация не найдена", content), status=404)

    status = "активна" if rec.is_active else "отклонена"
    badge = "bg-success" if rec.is_active else "bg-secondary"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Рекомендация №{rec.id}</h5>
            <p class="card-text">Пользователь: {rec.user.name} ({rec.user.email})</p>
            <p class="card-text">Маршрут: {rec.route.name}, {rec.route.info}</p>
            <p class="card-text">Релевантность: {rec.score}</p>
            <p class="card-text">Статус: <span class="badge {badge}">{status}</span></p>
            <a href="/recommendations/" class="btn btn-outline-secondary">
                ← к списку рекомендаций
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Рекомендация №{rec.id}", content), status=200)
