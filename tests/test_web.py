"""Проверка страниц Django: данные приходят из data/city_routes.sqlite."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "city_routes.settings")
django.setup()

from django.test import Client  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

setup_test_environment()  # сохраняет response.context для проверок


@pytest.fixture
def client():
    return Client(HTTP_HOST="localhost")


@pytest.mark.parametrize("url", [
    "/",
    "/routes/",
    "/routes/1/",
    "/routes/search/",
    "/recommendations/",
    "/recommendations/2/",
    "/recommendations/pick/",
    "/recommendations/statistics/",
])
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


@pytest.mark.parametrize("url", ["/routes/999/", "/recommendations/999/"])
def test_missing_objects_404(client, url):
    assert client.get(url).status_code == 404


def test_routes_list_from_db(client):
    response = client.get("/routes/")
    assert "Исторический центр" in response.content.decode()
    assert len(response.context["routes"]) == 6


def test_search_filters(client):
    response = client.get("/routes/search/", {"interest": "парки", "max_km": "3.5"})
    names = [row["name"] for row in response.context["routes"]]
    assert names == ["Парки Замоскворечья"]


def test_search_bad_number(client):
    response = client.get("/routes/search/", {"max_km": "много"})
    assert response.context["error"]


def test_pick_skips_active_recommendations(client):
    response = client.get("/recommendations/pick/", {"user": "4"})
    assert [row["name"] for row in response.context["routes"]] == ["Сталинские высотки"]


def test_statistics_having(client):
    response = client.get("/recommendations/statistics/", {"min": "1"})
    assert [row["route_name"] for row in response.context["popular"]] == ["Исторический центр"]
    response = client.get("/recommendations/statistics/", {"min": "5"})
    assert list(response.context["popular"]) == []
