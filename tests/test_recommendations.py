from recommendations import (
    create_recommendation,
    dismiss_recommendation,
    is_route_recommended,
    recommend_routes,
)

ROUTE = {"id": 1, "name": "Центр", "interest": "архитектура", "length_km": 4.5, "points_count": 6}
OTHER = {"id": 2, "name": "Парки", "interest": "парки", "length_km": 3.0, "points_count": 4}
USER = {"id": 1, "name": "Артур", "email": "a@example.com", "interest": "архитектура"}


def test_recommend_routes():
    assert recommend_routes([ROUTE, OTHER], USER) == [ROUTE]


def test_create_recommendation():
    recs = []
    rec = create_recommendation(recs, ROUTE, USER)
    assert rec is not None
    assert is_route_recommended(recs, 1, 1)


def test_interest_mismatch():
    assert create_recommendation([], OTHER, USER) is None


def test_duplicate_forbidden_until_dismissed():
    recs = []
    first = create_recommendation(recs, ROUTE, USER)
    assert create_recommendation(recs, ROUTE, USER) is None
    assert dismiss_recommendation(recs, first["id"])
    assert len(recs) == 1
    assert create_recommendation(recs, ROUTE, USER) is not None
