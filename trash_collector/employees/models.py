from django.db import models

# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employees(models.Model):
    name = models.CharField(max_length=50, default=("temp"))
    zip_code = models.CharField(max_length=10, null=True)