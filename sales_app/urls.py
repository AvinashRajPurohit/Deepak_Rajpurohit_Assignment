from django.urls import path
from sales_app.views import (update_user_and_sales_data, 
                             get_statistics_info, 
                             StatisticsView,
                             SaleListCreateAPIView,
                             SalesRetrieveUpdateView,
                             SalesDestroyView)

urlpatterns = [
  path("sales/update/<int:id>/user/", update_user_and_sales_data, name='update-user-sales'),
  path("sales/statistics/<int:user_id>", get_statistics_info, name="user-stats"),
  path("sale_statistics/", StatisticsView.as_view(), name='stats'),
  path("sales/", SaleListCreateAPIView.as_view(), name='sales-list'),
  path("sales/<int:id>", SalesRetrieveUpdateView.as_view(), name='get-update-sales'),
  path("sales/<int:id>/", SalesDestroyView.as_view(), name='delete-sales'),
]
