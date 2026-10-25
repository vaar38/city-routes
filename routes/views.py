from django.http import HttpResponse

from homepage.views import page
from models.routes import find_route_by_id, sort_routes
from storage import load_routes

SHORT_WALK_KM = 5


def routes(request):
    items = ""
    for route in sort_routes(load_routes()):
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/routes/{route.id}/">{route.name}</a>
            <span>{route.interest}, {route.info}</span>
        </li>
        """
    content = f"""
    <h1>Маршруты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("City Routes – маршруты", content))


def route_detail(request, route_id):
    route = find_route_by_id(load_routes(), route_id)
    if route is None:
        content = """
        <h1 class="text-danger">Маршрут не найден</h1>
        <a href="/routes/" class="btn btn-outline-secondary">← к списку маршрутов</a>
        """
        return HttpResponse(page("Маршрут не найден", content), status=404)

    short = route.is_suitable_for(SHORT_WALK_KM)
    badge = "bg-success" if short else "bg-warning text-dark"
    walk = "короткая прогулка" if short else "длинная прогулка"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{route.name}</h5>
            <p class="card-text"><strong>ID:</strong> {route.id}</p>
            <p class="card-text"><strong>Тематика:</strong> {route.interest}</p>
            <p class="card-text"><strong>Протяжённость:</strong> {route.length_km} км</p>
            <p class="card-text"><strong>Точек:</strong> {route.points_count}</p>
            <p class="card-text"><span class="badge {badge}">{walk}</span></p>
            <a href="/routes/" class="btn btn-outline-secondary">← к списку маршрутов</a>
        </div>
    </div>
    """
    return HttpResponse(page(route.name, content), status=200)
