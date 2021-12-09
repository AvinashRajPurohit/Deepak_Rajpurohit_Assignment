from rest_framework import generics, status, permissions
from rest_framework.response import Response
from users.serializers import LoginSerializer, LogoutSerializer, UserSerializer
from rest_framework.views import APIView
from users.models import Users
from django.shortcuts import get_object_or_404


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        user_serializer = UserSerializer(request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(user_serializer.data, status=status.HTTP_200_OK)



class UsersListAndSingleView(APIView):

  def get(self, request, id= None):
    if id==None:
      queryset = Users.objects.all()
      serializer = UserSerializer(queryset, many=True)
      return Response(serializer.data)
    else:
      queryset = get_object_or_404(Users, id=id)
      serializer = UserSerializer(queryset)
      return Response(serializer.data)
