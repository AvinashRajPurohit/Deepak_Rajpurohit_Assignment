from django.urls import path
from sales_app.views import (index, update_user_and_sales_data, 
                             get_statistics_info, 
                             StatisticsView,
                             SalesListView,
                             sales_delete,
                             SaleUpdateAPIView,
                             SaleCreateAPIView, index)

urlpatterns = [
  path('', index, name='index'),
  path("sales/update/<int:id>/user/", update_user_and_sales_data, name='update-user-sales'),
  path("sales/statistics/<int:user_id>", get_statistics_info, name="user-stats"),
  path("sales/statistics/", StatisticsView.as_view(), name='stats'),
  path("sales/list/", SalesListView.as_view(), name='sales-list'),
  path("sales/delete/<int:sales_id>", sales_delete, name='delete-sale'),
  path("sales/update/<int:sales_id>", SaleUpdateAPIView.as_view(), name='update-sale'),
  path('sales/create/', SaleCreateAPIView.as_view(), name='sales-create')
]