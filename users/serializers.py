from rest_framework import serializers
from users.models import City, Country, Users


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['email', 'password']


class LoginResponse(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'gender', 'age', 'country', 'city']

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
        fields = ['id', 'name', 'cities']

        def get_cities(self, obj):
            cities = City.objects.filter(
                        country=obj,
                    )
            serializer = CitySerializer(cities, many=True)

            return serializer.data
