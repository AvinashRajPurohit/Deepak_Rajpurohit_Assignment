from django.contrib import auth
from django.db.models import fields
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from users.models import City, Country, Users

class LoginSerializer(serializers.ModelSerializer):

  class Meta:
    model = Users
    fields = ['email', 'password', 'username', 'tokens']

  email = serializers.EmailField(max_length=255, min_length=3)
  password = serializers.CharField(
      max_length=68, min_length=6, write_only=True)
  username = serializers.CharField(
      max_length=255, min_length=3, read_only=True)

  tokens = serializers.SerializerMethodField()

  def get_tokens(self, obj):
      user = Users.objects.get(email=obj['email'])

      return {
          'user_id': user.id,
          'refresh': user.tokens()['refresh'],
          'access': user.tokens()['access']
      }

  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')
    user = auth.authenticate(email=email, password=password)

    if not user:
        raise AuthenticationFailed('Invalid credentials, try again')
    if not user.is_active:
        raise AuthenticationFailed('Account disabled, contact admin')

    return {
        'email': user.email,
        'data': user.tokens
    }




class LogoutSerializer(serializers.Serializer):
  email = serializers.EmailField()
  refresh = serializers.CharField()

  default_error_message = {
      'bad_token': ('Token is expired or invalid')
  }

  def validate(self, attrs):
    self.token = attrs['refresh']
    return attrs

  def save(self, **kwargs):

    try:
      RefreshToken(self.token).blacklist()
    except TokenError:
      self.fail('bad_token')



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['id', 'username', 
              'first_name', 'last_name', 
              'email', 'gender', 'age',
              'country', 'city']
              
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class CitySerializer(serializers.ModelSerializer):
  class Meta:
    model = City
    fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
      model = Country
      fields = ['name', 'cities']
    

    def get_cities(self, obj):
      cities = City.objects.filter(
                  country=obj,
              )

      serializer = CitySerializer(cities, many=True)

      return serializer.data


