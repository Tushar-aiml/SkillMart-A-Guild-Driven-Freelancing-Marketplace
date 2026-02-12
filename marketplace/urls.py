from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("client/", views.client_dashboard, name="client_dashboard"),
    path("worker/", views.worker_dashboard, name="worker_dashboard"),
    path("quests/", views.quest_list, name="quest_list"),
    path("quests/create/", views.quest_create, name="quest_create"),
    path("quests/<int:pk>/", views.quest_detail, name="quest_detail"),
    # JSON-style endpoints
    path("api/quests/<int:pk>/accept/", views.accept_quest_api, name="accept_quest_api"),
    path(
        "api/quests/<int:pk>/complete/",
        views.complete_quest_api,
        name="complete_quest_api",
    ),
    path(
        "api/quests/<int:pk>/review/",
        views.review_quest_api,
        name="review_quest_api",
    ),
]

