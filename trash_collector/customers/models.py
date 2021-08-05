from django.db import models
# Create your models here.

# TODO: Finish customer model by adding necessary properties to fulfill user stories


class Customer(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=5)
    pickup_day = models.CharField(max_length=10, null=True, default='Thursday')
    onetime_pickup = models.DateField(null=True, blank=True)
    start_supsension = models.DateField(null=True, blank=True)
    end_supsension = models.DateField(null=True, blank=True)
    balance = models.IntegerField(default=0)
    suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.name