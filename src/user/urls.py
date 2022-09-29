from django.urls import path
from django.contrib.auth import views as defaultViews

from user import views


urlpatterns = [
    #/users/login
    path("login/", defaultViews.LoginView.as_view(), name="login"),
    #/users/logout
    path("logout/", views.LogoutView.as_view(), name="logout"),
    #/users/profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #/users/signup
    path('signup/', views.SignUpView.as_view(), name='signup'),
    #/users/edit
    path("edit/",views.EditUserView.as_view(),name='edit_user'),
    #/users/password_change
    path(
        "password_change/", defaultViews.PasswordChangeView.as_view(), name="password_change"
    ),
    #/users/password_change/done
    path(
        "password_change/done/",
        defaultViews.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    #/users/password_reset
    path("password_reset/", defaultViews.PasswordResetView.as_view(), name="password_reset"),
    #/users/password_reset/done
    path(
        "password_reset/done/",
        defaultViews.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    )
]