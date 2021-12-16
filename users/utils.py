from django.contrib.auth import authenticate
from rest_framework import serializers


def get_and_authenticate_user(email, password):
    """
    This function will authenticate the user.
    email: email of user
    password: password of user
    """
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user