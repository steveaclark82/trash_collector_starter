from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Customer
from django.urls import reverse
from datetime import date

def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user

    try:
        # This line inside the 'try' will return the customer record of the logged-in user if one exists
        logged_in_customer = Customer.objects.get(user=user)
    except:
        # TODO: Redirect the user to a 'create' function to finish the registration process if no customer record found
        return render(request, 'customers/create.html')

    # It will be necessary while creating a Customer/Employee to assign request.user as the user foreign key

    print(user)
    return render(request, 'customers/index.html', context={"logged_in_customer": logged_in_customer})



def create(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        pickup_day = request.POST.get('pickup_day')
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        customer = Customer()
        customer.user = user
        customer.name = name
        customer.balance = 0
        customer.pickup_day = pickup_day
        customer.zipcode = zipcode
        customer.address = address
        customer.save()
        return render(request, 'customers/index.html', context={'customer': customer})
    else:
        return render(request, 'customers/create.html')
