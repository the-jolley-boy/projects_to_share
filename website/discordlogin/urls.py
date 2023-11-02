from django.urls import path
from . import views

urlpatterns = [
    path("", views.notify, name="notify"),
    path("staff_data/", views.staff_data, name="staff_data"),
    path("betting/", views.betting, name="betting"),
    path("release_channel_generator/", views.release_channel_generator, name="release_channel_generator"),
    path("weekly_calendar/", views.weekly_calendar, name="weekly_calendar"),
    path("monthly_calendar/", views.monthly_calendar, name="monthly_calendar"),
    path("release_intro/", views.release_intro, name="release_intro"),
    path("login/", views.discord_login, name="oauth2_login"),
    path("login/redirect", views.discord_login_redirect, name="discord_login_redirect"),
]