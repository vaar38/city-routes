from models import Recommendation, Route, User
from storage import (
    load_json,
    load_recommendations,
    load_routes,
    save_json,
    save_recommendations,
    save_routes,
)


def test_save_and_load(tmp_path):
    path = tmp_path / "items.json"
    save_json(path, [{"id": 1, "name": "Центр"}])
    assert load_json(path) == [{"id": 1, "name": "Центр"}]


def test_missing_file(tmp_path):
    assert load_json(tmp_path / "nope.json") == []


def test_broken_file(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{oops", encoding="utf-8")
    assert load_json(path) == []


def test_routes_round_trip(tmp_path):
    path = tmp_path / "routes.json"
    save_routes([Route(1, "Центр", "архитектура", 4.5, 6)], path)
    routes = load_routes(path)
    assert isinstance(routes[0], Route)
    assert routes[0].length_km == 4.5


def test_recommendations_restore_links(tmp_path):
    path = tmp_path / "recs.json"
    route = Route(1, "Центр", "архитектура", 4.5, 6)
    user = User(1, "Артур", "a@example.com", "архитектура")
    save_recommendations([Recommendation(1, route, user)], path)
    assert load_json(path)[0]["route_id"] == 1
    recs = load_recommendations([route], [user], path)
    assert recs[0].route is route
    assert recs[0].user is user


def test_recommendation_with_missing_route_skipped(tmp_path):
    path = tmp_path / "recs.json"
    save_json(path, [{"id": 1, "route_id": 9, "user_id": 1}])
    user = User(1, "Артур", "a@example.com", "архитектура")
    assert load_recommendations([], [user], path) == []
