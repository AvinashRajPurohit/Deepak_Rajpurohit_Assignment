import pandas as pd
from users.forms import UserRegistrationForm
from django.contrib import messages
from sales_app.models import Sales
from users.models import Users
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from sales_app.utils import get_sales_plot
from sales_app.serializers import SalesSerializer
from django.shortcuts import (get_object_or_404,
                              redirect, render)


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

    if request.method == 'POST':
        # handling the operation of sales csv file bulk insert
        if 'sales_submit' in request.POST:
            csv_file = request.FILES.get("sales_file")
            dict_data = pd.read_csv(csv_file).to_dict('records')
            insert_data_in_sales_model(dict_data, id)
            messages.success(request, "Sales data has been \
                                       inserted successfully...")
            return redirect("user-stats", user_id=id)

        # handling the operation of update the user information
        elif 'user_submit' in request.POST:
            form = UserRegistrationForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Sales User has been \
                                           updated successfully...")
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
    sales_result = sales.values('product').order_by(
                  'product').annotate(total_sales=Sum('sales_number'))
    for p in sales_result:
        products.append(p['product'])
        total_sales.append(p['total_sales'])

    # here we get the chart using get_sales_plot
    chart = get_sales_plot(products, total_sales)

    context = {"u_info": user,
               "sales": sales,
               "chart": chart}

    return render(request, 'statistics.html', context)


class StatisticsView(APIView):
    """
    Api view for giving all the statistics of sales 
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        it will get the statistics
        """
        final_response = {}
        sales = Sales.objects.all()
        total_revenue = sales.aggregate(Sum('revenue'))['revenue__sum']
        user_sales = sales.filter(user=request.user)
        final_response['average_sales_for_current_user'] = self.average_sales_for_current_user(user_sales)
        final_response['average_sale_all_user'] = total_revenue/sales.count()
        final_response['highest_revenue_sale_for_current_user'] = self.highest_revenue_sale_for_current_user(user_sales)
        final_response['product_highest_revenue_for_current_user'] = self.product_highest_revenue_for_current_user(user_sales)
        final_response['product_highest_sales_number_for_current_user'] = self.product_highest_sales_number_for_current_user(user_sales)
        return Response(final_response)

    @staticmethod
    def average_sales_for_current_user(user_sales):
        """average sales for current user (Divide the total revenue
        for all the sales by the number of sales for that user)"""
        try:
            total_user_revenue = user_sales.aggregate(Sum('revenue'))
            rev_sum = total_user_revenue['revenue__sum']
            return rev_sum/user_sales.count()
        except Exception as e:
            return str(e)

    @staticmethod
    def highest_revenue_sale_for_current_user(user_sales):
        """this function give the heighest revenue sale for current user"""
        try:
            highest_revenue_sale = user_sales.order_by('-revenue')[0]
            data = {"sale_id": highest_revenue_sale.id,
                    "revenue": highest_revenue_sale.revenue}
            return data
        except Exception as e:
            return str(e)

    @staticmethod
    def product_highest_revenue_for_current_user(user_sales):
        """
        this function product highest revenue for current user
        """
        try:
            revenue_dict = {}
            revenue_result = user_sales.values('product').order_by(
              'product').annotate(total_revenue=Sum('revenue'))

            for i in revenue_result:
                revenue_dict[i['product']] = i['total_revenue']
            max_key = max(zip(revenue_dict.values(), revenue_dict.keys()))[1]
            data = {"product_name": max_key,
                    "price": revenue_dict[max_key]}
            return data
        except Exception as e:
            return str(e)

    @staticmethod
    def product_highest_sales_number_for_current_user(user_sales):
        """this function will give product
        highest sales number for current user"""
        try:
            sales_dict = {}
            sale_result = user_sales.values('product').order_by(
                'product').annotate(total_sales=Sum('sales_number'))
            for i in sale_result:
                sales_dict[i['product']] = i['total_sales']
            max_sale = max(zip(sales_dict.values(), sales_dict.keys()))[1]
            data = {"product_name": max_sale,
                    "price": sales_dict[max_sale]}
            return data
        except Exception as e:
            return str(e)


class SalesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    This api help to get update and delete the sales object
    """
    lookup_field = 'id'
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class SaleListCreateAPIView(generics.ListCreateAPIView):
    """
    This api view for creating the sales object
    and giving the list of sales objects
    """
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


def index(request):
    """
    This is home view which have information about application.
    request: django.core.handlers.wsgi.WSGIRequest
    """
    return render(request, 'index.html')
