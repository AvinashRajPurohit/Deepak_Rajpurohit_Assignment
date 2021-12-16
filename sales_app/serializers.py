from rest_framework import serializers
from sales_app.models import Sales


class SalesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Sales
        exclude = ('user', )

    def get_user_id(self, obj):
        user_id = self.user.id
        return user_id
