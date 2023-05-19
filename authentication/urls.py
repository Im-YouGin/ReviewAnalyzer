from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "email-confirm/<str:token>/",
        views.EmailConfirmView.as_view(),
        name="confirm-email",
    ),
    path(
        "password-change/", views.PasswordChangeView.as_view(), name="password-change"
    ),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
