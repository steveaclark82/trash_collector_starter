from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Customer
from django.urls import reverse
from datetime import date

today = date.today()
today = today.strftime("%Y-%m-%d")

# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    user = request.user

    if not Customer.objects.filter(user_id=user.id).exists():
            return redirect('create/')
    else:
        specific_customer = Customer.objects.get(user_id=user.id)
        context = {
            'user': user,
            'specific_customer': specific_customer
        }
        print(user)
        return render(request, 'customers/index.html', context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        weekly_pickup_day = request.POST.get('weekly_pickup_day')
        address = request.POST.get('address')
        zip_code = request.POST.get('zip_code')
        one_time_pickup = request.POST.get('one_time_pickup')
        new_customer = Customer(
            user_id=request.user.id,
            name=name,
            weekly_pickup_day=weekly_pickup_day,
            onetime_pickup=one_time_pickup,
            address=address,
            zip_code=zip_code,
        )
        new_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/create.html')


def edit(request, option):
    specific_option = option
    user = request.user
    specific_customer = Customer.objects.get(user_id=user.id)
    context = {
        'specific_customer': specific_customer,
        'specific_option': specific_option
    }
    if request.method == 'POST':
        if specific_option == 1:
            # For Weekly pickup
            specific_customer.weekly_pickup_day = request.POST.get('weekly_pickup_day')
            specific_customer.save()
        elif specific_option == 2:
            # For Suspended account
            specific_customer.start_suspension = request.POST.get('start_suspension')
            specific_customer.end_suspension = request.POST.get('end_suspension')
            specific_customer.save()
            start = specific_customer.start_suspension
            end = specific_customer.end_suspension
            if end > today:
                specific_customer.has_suspension = True
            elif start > today:
                specific_customer.has_suspension = False
            elif end == today:
                specific_customer.has_suspension = False
            else:
                specific_customer.has_suspension = False

            specific_customer.save()
        elif specific_option == 3:
            # For Onetime pickup
            specific_customer.onetime_pickup = request.POST.get('onetime_pickup')
            specific_customer.save()
        elif specific_option == 4:
            # For Editing Account Info
            specific_customer.name = request.POST.get('name')
            specific_customer.address = request.POST.get('address')
            specific_customer.zip_code = request.POST.get('zip_code')
            specific_customer.save()

        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/edit.html', context)