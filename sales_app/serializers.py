from django.db.models import fields
from rest_framework import serializers
from sales_app.models import Sales

class SalesSerializer(serializers.ModelSerializer):

  class Meta:
    model = Sales
    fields = '__all__'