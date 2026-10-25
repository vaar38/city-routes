import pytest

from routes import (
    add_route,
    check_route_length,
    delete_route,
    filter_routes_by_length,
    find_route,
    sort_routes,
)


def make_routes():
    routes = []
    add_route(routes, "Исторический центр", "Архитектура", 4.5, 6)
    add_route(routes, "Парки", "парки", 3.0, 4)
    return routes


def test_add_route():
    routes = make_routes()
    assert len(routes) == 2
    assert routes[1]["id"] == 2
    assert routes[0]["interest"] == "архитектура"


def test_add_route_invalid_length():
    with pytest.raises(ValueError):
        add_route([], "Маршрут", "парки", 0, 3)


def test_find_route():
    assert len(find_route(make_routes(), "центр")) == 1


def test_check_route_length():
    routes = make_routes()
    assert check_route_length(routes, 1, 5)
    assert not check_route_length(routes, 1, 4)


def test_filter_and_sort():
    routes = make_routes()
    assert [r["id"] for r in filter_routes_by_length(routes, 3.5)] == [2]
    assert [r["id"] for r in sort_routes(routes)] == [2, 1]


def test_delete_route():
    routes = make_routes()
    assert delete_route(routes, 1)
    assert not delete_route(routes, 1)
    assert len(routes) == 1
