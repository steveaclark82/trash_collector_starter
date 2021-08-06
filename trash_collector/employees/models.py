from django.db import models
# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.Employee', blank=True, null=True, on_delete=models.CASCADE)
    zip_code = models.CharField(length=5)
    customer_list = models.CharField(models.list)

    def __str__(self):
        return self.employee_name
