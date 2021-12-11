from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from users.serializers import LoginSerializer, LogoutSerializer, UserSerializer, CountrySerializer
from rest_framework.views import APIView
from users.models import Country, Users
from django.shortcuts import get_object_or_404, redirect, render
from users.forms import UserRegistrationForm
from django.contrib import messages


class LoginAPIView(generics.GenericAPIView):
  """
  Api for user login
  """
  serializer_class = LoginSerializer

  def post(self, request):
      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
  """
  This will logout the user.
  """
  serializer_class = LogoutSerializer

  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):

    serializer = self.serializer_class(data=request.data)
    user_serializer = UserSerializer(request.user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(user_serializer.data, status=status.HTTP_200_OK)


class UsersListAndSingleView(APIView):

  """
  Api view for lising user or getting single user
  """

  def get(self, request, id= None):
    """
    it will get the list of user or give the single user data
    id: id of the user
    """
    if id==None:
      # fetch all user
      queryset = Users.objects.all()
      serializer = UserSerializer(queryset, many=True)
      return Response(serializer.data)
    else:
      # get a user
      queryset = get_object_or_404(Users, id=id)
      serializer = UserSerializer(queryset)
      return Response(serializer.data)


def add_user(request):
  """
  This view will add an sales user
  request: django request
  """
  form = UserRegistrationForm()
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      password = form.data.get("password") # Storing hashed password
      f = form.save(commit=False)
      f.set_password(password)
      f.save()
      messages.success(request, "Sales User has been add successfully...")
      return redirect("add-user")
    else:
      messages.success(request, "Data submission is not valid...")
      return redirect("add-user")
      
  context = {
    "user_form": form
  }
  return render(request, 'add_user.html', context)



def list_users(request):
  """
  This view will give the list all sales users
  request: django request
  """

  users = Users.objects.all()
  context = {"users": users}
  return render(request, 'list_users.html', context)





class CountryListView(APIView):
  
  """
  Api view for lising all the countires and their cities
  """

  def get(self, request):
    """
    it will get the list all the countires and their cities
    """
    # fetch all countries
    queryset = Country.objects.all()
    serializer = CountrySerializer(queryset, many=True)
    return Response(serializer.data)


class UpdateUserView(APIView):
  
  """
  Api view for updateing user
  """

  def get(self, request):
    """
    it will get the list of user or give the single user data
    """
    # fetch all countries
    queryset = Country.objects.all()
    serializer = CountrySerializer(queryset, many=True)
    return Response(serializer.data)


class UserUpdateAPIView(generics.UpdateAPIView):
  """
  This viewset will partial update user
  """
  serializer_class = UserSerializer

  def update(self, request, user_id, *args, **kwargs):
    user = get_object_or_404(Users, id=user_id)
    serializer = self.serializer_class(user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)