from django.db import models
# Create your models here.

# TODO: Create an Employee model with properties required by the user stories

<<<<<<< HEAD
class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.Employee', blank=True, null=True, on_delete=models.CASCADE)
    zip_code = models.CharField(length=5)
    customer_list = models.CharField(models.list)

    def __str__(self):
        return self.employee_name
=======
class Employees(models.Model):
    name = models.CharField(max_length=50, default="")
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.PROTECT)
    zip_code = models.IntegerField(default=00000, null=True)
    todays_customers = []

>>>>>>> parent of b50c532 (init)
