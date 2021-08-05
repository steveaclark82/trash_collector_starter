from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.apps import apps
from .models import Employees
from datetime import date

today = date.today()
the_current_day_of_week = today.strftime("%A")  # Monday, Tuesday, Wednesday, Thursday, Friday
today = today.strftime("%Y-%m-%d")

print(today)

from django.urls import reverse

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    Customer = apps.get_model('customers.Customer')
    user = request.user
    if not Employees.objects.filter(user_id=user.id).exists():
        return redirect('create/')
    else:
        all_customers = Customer.objects.all()
        specific_employee = Employees.objects.get(user_id=user.id)
        zip_code_customers = []
        todays_customers = []
        for customer in all_customers:
            if customer.zip_code == specific_employee.zip_code:
                zip_code_customers.append(customer)

        for customer in zip_code_customers:
            check_suspension(customer)
            if customer.has_suspension:
                zip_code_customers.pop()

        for customer in zip_code_customers:
            if customer.weekly_pickup_day == the_current_day_of_week \
                    or customer.onetime_pickup == today:
                todays_customers.append(customer)

        # one_time_pickup = same_zip_customers.filter(onetime_pickup=)
        specific_employee.save()
        context = {
            'user': user,
            'todays_customers': todays_customers,
            'specific_employee': specific_employee
        }
        # print(user)
        return render(request, 'employees/index.html', context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        zip_code = request.POST.get('zip_code')
        new_employee = Employees(
            user_id=request.user.id,
            name=name,
            zip_code=zip_code,
        )
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


def check_suspension(the_customer):
    start_date = the_customer.start_suspension
    end_date = the_customer.end_suspension
    start = start_date
    end = end_date
    if end is None:
        pass
    else:
        if end > today:
            the_customer.has_suspension = True
        elif start > today:
            the_customer.has_suspension = False
        elif end == today:
            the_customer.has_suspension = False
        else:
            the_customer.has_suspension = False
        the_customer.save()


def find_customers_by_day(request):
    user = request.user
    if request.method == 'POST':
        option = request.POST['day of week']
        print(option)
        Customer = apps.get_model('customers.Customer')
        specific_employee = Employees.objects.get(user_id=user.id)
        zip_code_customers = Customer.objects.filter(zip_code=specific_employee.zip_code)
        daily_customers = []
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for day in weekdays:
            if option == day:
                daily_customers = zip_code_customers.filter(weekly_pickup_day=day)
        context = {
            'daily_customers': daily_customers
        }
        return render(request, 'employees/filter_pickups.html', context)

    else:
        return render(request, 'employees/filter_pickups.html')


def confirmed_pickups(request, customer_id):
    Customer = apps.get_model('customers.Customer')

    all_customers = Customer.objects.all()
    specific_customer = all_customers.get(id=customer_id)
    specific_customer.balance += 10
    specific_customer.last_confirmed_pickup = today
    specific_customer.save()

    return HttpResponseRedirect(reverse('employees:index'))


"""
if option == 'Monday':
    daily_customers = zip_code_customers.filter(weekly_pickup_day='Monday')
elif option == 'Tuesday':
    daily_customers = zip_code_customers.filter(weekly_pickup_day='Tuesday')
elif option == 'Wednesday':
    daily_customers = zip_code_customers.filter(weekly_pickup_day='Wednesday')
elif option == 'Thursday':
    daily_customers = zip_code_customers.filter(weekly_pickup_day='Thursday')
elif option == 'Friday':
    daily_customers = zip_code_customers.filter(weekly_pickup_day='Friday')"""