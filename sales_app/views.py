from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from users.forms import UserRegistrationForm
from django.contrib import messages
from sales_app.models import Sales
from users.models import Users
import pandas as pd
# Create your views here.


def index(request):
  """
  This view will add the user
  request: django request
  """
  form = UserRegistrationForm()
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      f = form.save(commit=False)
      f.set_password("admin@123")
      f.save()
      messages.warning(request, "Sales User has been add successfully...")
      return redirect("add-user")
    else:
      print(form.errors)
  context = {
    "user_form": form
  }
  return render(request, 'index.html', context)


def insert_data_in_sales_model(data: list, user_id):
  """
  This function will insert data in sales model
  """
  user = get_object_or_404(Users, id=user_id)


  for row in data:
    row['user'] = user
    Sales.objects.create(**row)
  
  return "Data has been inserted successfully...."



def update_user(request, id):
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
      return redirect("update-user", id=id)
    elif 'user_submit' in request.POST:
      form = UserRegistrationForm(request.POST, instance=user)
      if form.is_valid():
        form.save()
        messages.success(request, "Sales User has been updated successfully...")
        return redirect("update-user", id=id)
      else:
        print(form.errors)
  context = {

    "user_form": form,
    "user_id": id

  }
  return render(request, 'update_user.html', context)