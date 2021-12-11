from django.shortcuts import get_object_or_404, redirect, render
from users.forms import UserRegistrationForm
from django.contrib import messages
from sales_app.models import Sales
from users.models import Users
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from sales_app.utils import get_sales_plot
from sales_app.serializers import SalesSerializer
from rest_framework.decorators import api_view
import pandas as pd
# Create your views here.


def insert_data_in_sales_model(data: list, user_id):
  """
  This function will insert data in sales model
  """
  user = get_object_or_404(Users, id=user_id)


  for row in data:
    row['user'] = user
    Sales.objects.create(**row)
  
  return "Data has been inserted successfully...."



def update_user_and_sales_data(request, id):
  """
  This view will update the user
  id: id of the user that we want to update
  request: django request
  """
  user = get_object_or_404(Users, id=id)
  form = UserRegistrationForm(instance=user)

  print(request.POST)
  print(request.method)
  if request.method == 'POST':
    if 'sales_submit' in request.POST:
      print('here')
      print(request.FILES)
      csv_file = request.FILES.get("sales_file")
      dict_data = pd.read_csv(csv_file).to_dict('records')
      insert_data = insert_data_in_sales_model(dict_data, id)
      print(insert_data)
      messages.success(request, "Sales data has been inserted successfully...")
      return redirect("user-stats", user_id=id)
    elif 'user_submit' in request.POST:
      form = UserRegistrationForm(request.POST, instance=user)
      if form.is_valid():
        form.save()
        messages.success(request, "Sales User has been updated successfully...")
        return redirect("user-stats", user_id=id)
      else:
        print(form.errors)
  context = {

    "user_form": form,
    "user_id": id

  }
  return render(request, 'update_user.html', context)


def get_statistics_info(request, user_id):
  """
  this function will return all the statistics related to sales user
  user_id : id of sales user
  request: django request
  """
  products = []
  total_sales = []
  # personal information
  user = get_object_or_404(Users, id=user_id)
  
  sales = Sales.objects.filter(user=user)

  # sales_number
  sales_result = sales.values('product').order_by('product').annotate(total_sales=Sum('sales_number'))
  for p in sales_result:
    products.append(p['product'])
    total_sales.append(p['total_sales'])

  chart = get_sales_plot(products, total_sales)
  context = {"u_info": user,
            "sales": sales,
            "chart": chart}

  return render(request, 'statistics.html', context)




class StatisticsView(APIView):
  
  """
  Api view for lising all the countires and their cities
  """
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request):
    """
    it will get the statistics
    """

    sales = Sales.objects.all()
    final_response = {}
    total_revenue = sales.aggregate(Sum('revenue'))['revenue__sum']
    # average sales for current user (Divide the total revenue for all the sales by the number of sales for that user)
    user_sales = sales.filter(user=request.user)
    total_user_revenue = user_sales.aggregate(Sum('revenue'))['revenue__sum']
    final_response['average_sale_current_user'] = total_user_revenue/user_sales.count()


    # average sale all user(Divide the total sales revenue for all users’ sales by the number of all sales.)
    final_response['average_sale_all_user'] = total_revenue/sales.count()


    # heighest revenue sale for current user
    highest_revenue_sale = user_sales.order_by('-revenue')[0]
    final_response['highest_revenue_sale_for_current_user'] = {"sale_id": highest_revenue_sale.id,
                                                                  "revenue": highest_revenue_sale.revenue}


    # product highest revenue for current user
    revenue_result = user_sales.values('product').order_by('product').annotate(total_revenue=Sum('revenue'))
    revenue_dict = {}

    for i in revenue_result:
      revenue_dict[i['product']] = i['total_revenue']
    max_key = max(zip(revenue_dict.values(), revenue_dict.keys()))[1]

    final_response['product_highest_revenue_for_current_user'] = {"product_name": max_key,
                                                                  "price": revenue_dict[max_key]}




    # product highes sales number for current user
    sale_result = user_sales.values('product').order_by('product').annotate(total_sales=Sum('sales_number'))
    sales_dict = {}

    for i in sale_result:
      sales_dict[i['product']] = i['total_sales']
    max_sale = max(zip(sales_dict.values(), sales_dict.keys()))[1]

    final_response['product_highest_sales_number_for_current_user'] = {"product_name": max_sale,
                                                                  "sales_number": sales_dict[max_sale]}


    
    return Response(final_response)


class SalesListView(APIView):
    
  """
  Api view for lising all the sales
  """

  def get(self, request):
    """
    it will get all the sales
    """
    # fetch all sales
    queryset = Sales.objects.all()
    serializer = SalesSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(["DELETE"])
def sales_delete(request, sales_id):
  """
  This api will delete the perticular sale object
  sales_id: id of sales that we want to delete
  """
  get_object_or_404(Sales, id=sales_id).delete()
  return Response(status=status.HTTP_204_NO_CONTENT)


class SaleUpdateAPIView(generics.UpdateAPIView):
  """
  This viewset will partial update sales
  """
  serializer_class = SalesSerializer

  def update(self, request, sales_id, *args, **kwargs):
    sale = get_object_or_404(Sales, id=sales_id)
    serializer = self.serializer_class(sale, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)



class SaleCreateAPIView(generics.CreateAPIView):
  """
  This api view for creating the sales object
  """
  queryset = Sales.objects.all()
  serializer_class = SalesSerializer


def index(request):
  return render(request, 'index.html')