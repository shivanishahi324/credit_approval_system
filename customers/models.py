from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    customer_id = models.IntegerField(unique=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    approved_limit = models.IntegerField(default=0)
    current_debt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

