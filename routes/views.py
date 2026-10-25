from django.shortcuts import render

from models.routes import find_route_by_id, sort_routes
from storage import load_routes

SHORT_WALK_KM = 5


def routes(request):
    context = {
        "routes": sort_routes(load_routes()),
    }
    return render(request, "routes/route_list.html", context)


def route_detail(request, route_id):
    route = find_route_by_id(load_routes(), route_id)
    context = {
        "route": route,
        "is_short": route is not None and route.is_suitable_for(SHORT_WALK_KM),
    }
    return render(
        request,
        "routes/route_detail.html",
        context,
        status=404 if route is None else 200,
    )
