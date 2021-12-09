from django.urls import path
from .views import LoginAPIView, LogoutAPIView, UsersListAndSingleView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path("list/", UsersListAndSingleView.as_view(), name='users-list'),
    path("<int:id>/", UsersListAndSingleView.as_view(), name='single-user'),



]