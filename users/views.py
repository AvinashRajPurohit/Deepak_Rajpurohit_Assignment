from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Country, Users
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import redirect, render
from users.forms import UserRegistrationForm
from django.contrib import messages
from users.utils import get_and_authenticate_user
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ObjectDoesNotExist
from users.serializers import (LoginSerializer,
                               UserSerializer,
                               CountrySerializer,
                               LoginResponse)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
LOGIN_API_DESCRIPTION = 'This api for login using email and password, \
                         and get token in response'


@swagger_auto_schema(method='post', request_body=LoginSerializer,
responses={'200': LoginResponse}, operation_description=LOGIN_API_DESCRIPTION)
@api_view(["POST"])
@permission_classes((AllowAny,))
@csrf_exempt
def login(request):
    """
    Api for user login
    """
    user_email = request.data.get('email', '')
    user_password = request.data.get('password', '')
    if user_email is None or user_password is None:
        message = 'Please provide both username and password'
        return Response({'error': message}, status=HTTP_400_BAD_REQUEST)
    user = get_and_authenticate_user(email=user_email, password=user_password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"user_id": user.id, 'token': token.key},
                    status=HTTP_200_OK)


def add_user(request):
    """
    This view will add an sales user
    request: django request
    """
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.data.get("password")  # Storing hashed password
            f = form.save(commit=False)
            f.set_password(password)
            f.save()
            messages.success(request, "Sales User has been"
                                      " add successfully...")
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


class LogoutAPIView(generics.GenericAPIView):
    """
    This will logout the user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        """
        this function will logout the user...
        """
        user_serializer = self.serializer_class(request.user)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        auth_logout(request)

        return Response(user_serializer.data, status=HTTP_200_OK)


class UsersRetriveUpdate(generics.RetrieveUpdateAPIView):
    """
    This api view for getting single user and updating user
    """
    lookup_field = 'id'
    queryset = Users.objects.all()
    serializer_class = UserSerializer


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
