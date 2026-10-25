from django.urls import path

from . import views

app_name = "recommendations"

urlpatterns = [
    path("", views.recommendations, name="list"),
    path("pick/", views.pick, name="pick"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:rec_id>/", views.recommendation_detail, name="detail"),
]
