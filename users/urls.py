from django.urls import path
from .views import (LoginAPIView,
                    LogoutAPIView, 
                    UsersListAndSingleView, 
                    add_user, list_users,
                    CountryListView,
                    UserUpdateAPIView)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('users/login/', LoginAPIView.as_view(), name="login"),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', LogoutAPIView.as_view(), name="logout"),
    path("users/list/", UsersListAndSingleView.as_view(), name='users-list'),
    path("users/<int:id>/", UsersListAndSingleView.as_view(), name='single-user'),
    path("countries/", CountryListView.as_view(), name='country-list'),
    path("users/add/", add_user, name='add-user'),
    path("users/all/", list_users, name='all-user'),
    path("users/update/<int:user_id>", UserUpdateAPIView.as_view(), name='user-update')





]