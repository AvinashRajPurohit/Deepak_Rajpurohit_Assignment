from django.urls import path
from sales_app.views import index, update_user

urlpatterns = [
  path("add_sales_user/", index, name='add-user'),
  path("update_user/<int:id>", update_user, name='update-user')
]