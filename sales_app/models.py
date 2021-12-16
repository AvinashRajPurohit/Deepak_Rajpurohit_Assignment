from django.db import models
from users.models import Users
# Create your models here.


class Sales(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    sales_number = models.PositiveIntegerField()
    revenue = models.FloatField()
    date = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.user.email} product -{self.product} \
                  revenue - {self.revenue}"
