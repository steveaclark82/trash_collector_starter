from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Customer
from django.urls import reverse
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")

# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user

    try:
        # This line inside the 'try' will return the customer record of the logged-in user if one exists
        logged_in_customer = Customer.objects.get(user=user)
        context = {
            'logged_in_customer': logged_in_customer
        }
        return render(request, 'customer/account.html', context)
    except:
        return HttpResponseRedirect(reverse('customer:register'))
        pass

    # It will be necessary while creating a Customer/Employee to assign request.user as the user foreign key

    print(user)
    return render(request, 'customers/index.html')

def account_info(request):
    user = request.user
    customer = Customer.objects.get(user=user.id)
    context = {
        'customer': customer
    }
    return render(request, 'customers/account.html', context)

def onetime_pickup(request):
    user = request.user
    customer = Customer.objects.get(user=user.id)
    if request.method == 'POST':
        customer.onetime_pickup = request.POST.get('pickup')
        customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/one_time_pickup.html')

def create_customer(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        pickup_date = request.POST.get('pickup_date')
        balance = request.POST.get('balance')
        zipcode = request.POST.get('zipcode')
        address = request.POST.get('address')
        new_customer = Customer(name=name, pickup_date=pickup_date,
                                balance=balance, zipcode=zipcode, address=address, user_id=user.id)
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/register.html')

def suspend_pickup(request):
    user = request.user
    customer = Customer.objects.get(user=user.id)
    if request.method == 'POST':
        customer.start_date = request.POST.get('start')
        customer.end_date = request.POST.get('end')
        customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/suspend_pickup.html')

def weekly_pickup(request):
    user = request.user
    customer = Customer.objects.get(user=user.id)
    if request.method == 'POST':
        customer.pickup_date = request.POST.get('name')
        customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/weekly_pickup.html')


