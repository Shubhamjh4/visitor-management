from django.urls import path
from .views import IntakeView, visit_detail, end_visit, dashboard, guard_visit_detail, health_check


urlpatterns = [
    path("", IntakeView.as_view(), name="intake"),
    path("visit/<int:visit_id>/", visit_detail, name="visit_detail"),
    path("visit/<int:visit_id>/end/", end_visit, name="end_visit"),
    # Custom admin-like dashboard path not visible from public pages
    path("control/", dashboard, name="dashboard"),
    path("control/visit/<int:visit_id>/", guard_visit_detail, name="guard_visit_detail"),
    # Health check endpoint for keeping service warm
    path("health/", health_check, name="health_check"),
]


