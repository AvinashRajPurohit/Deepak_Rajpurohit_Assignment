from django.urls import path, include
from .views import (LogoutAPIView, UsersRetriveUpdate, add_user,
                    list_users, login, CountryListView)

urlpatterns = [
    path('', include('sales_app.urls')),
    path('login/', login, name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path("users/<int:id>/", UsersRetriveUpdate.as_view(), name='single-user'),
    path("countries/", CountryListView.as_view(), name='country-list'),
    path("users/add/", add_user, name='add-user'),
    path("users/all/", list_users, name='all-user'),
]
