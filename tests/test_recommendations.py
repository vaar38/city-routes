from models import Recommendation, Route, User
from models.recommendations import (
    create_recommendation,
    dismiss_recommendation,
    is_route_recommended,
    recommend_routes,
)

ROUTE = Route(1, "Центр", "архитектура", 4.5, 6)
OTHER = Route(2, "Парки", "парки", 3.0, 4)
USER = User(1, "Артур", "a@example.com", "архитектура")


def test_recommendation_links_objects():
    rec = Recommendation(1, ROUTE, USER)
    assert rec.route is ROUTE
    assert rec.user is USER
    assert rec.is_active
    assert str(rec) == "Артур → Центр [активна]"


def test_dismiss_method():
    rec = Recommendation(1, ROUTE, USER)
    rec.dismiss()
    assert rec.is_dismissed
    assert "отклонена" in str(rec)


def test_recommend_routes():
    assert recommend_routes([ROUTE, OTHER], USER) == [ROUTE]


def test_create_recommendation():
    recs = []
    rec = create_recommendation(recs, ROUTE, USER)
    assert rec is not None
    assert is_route_recommended(recs, ROUTE, USER)


def test_interest_mismatch():
    assert create_recommendation([], OTHER, USER) is None


def test_duplicate_forbidden_until_dismissed():
    recs = []
    first = create_recommendation(recs, ROUTE, USER)
    assert create_recommendation(recs, ROUTE, USER) is None
    assert dismiss_recommendation(recs, first.id)
    assert len(recs) == 1
    assert create_recommendation(recs, ROUTE, USER) is not None
