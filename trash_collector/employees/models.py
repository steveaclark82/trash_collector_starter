from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employee(models.Model):
    name = models.CharField(max_length=50, default=("temp"))
    zip_code = models.CharField(max_length=10, null=True)
    user = models.ForeignKey('account.User', blank=True, null=True, on_delete=models.CASCADE)