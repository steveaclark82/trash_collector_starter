from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps
from .models import Employee
from datetime import date
import calendar
from django.db.models import Q
from django.urls import reverse

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    Customer = apps.get_model('customers.Customer')
    user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=user)
    except:
        return render(request, 'employee/create.html')
    employee_customers = customers.objects.filter(Q(zip_code=logged_in_employee.zip_code,
                                                    pickup_day=calendar.day_name[date.today().weekday()]) | Q(~Q(pickup_day=calendar.day_name[date.today().weekday()]), one_time_pickup=date.today())).exclude(Q((Q(suspension_start__lte=date.today()) & Q(suspension_end__gte=date.today())) & ~Q(one_time_pickup=date.today())))
    context = {
        'employee_customers': employee_customers,
        'logged_in_employee': logged_in_employee
    }
    return render(request, 'employees/index.html', context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        zip_code = request.POST.get('zip_code')
        new_employee = Employee(name=name, zip_code=zip_code, user=request.user)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


def confirm_pickups(request, customer_id):
    if request.method == 'POST':
        customers = apps.get_model('customers.Customer')
        customer = customers.objects.get(id=customer_id)
        customer.account_balance += 15
        customer.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/index.html')


def filter_pickups(request):
    customers = apps.get_model('customers.Customer')
    employee = Employee.objects.get(user=request.user)
    employee_customers = customers.objects.filter(zip_code=employee.zip_code)
    if request.method == 'POST':
        filtered_customers = customers.objects.filter(zip_code=employee.zip_code).filter(pickup_day=request.POST.get('pickup_day'))
        context = {
            'customers': filtered_customers,
            'employee': employee
        }
        return render(request, 'employees/filter_pickups.html', context)
    else:
        context = {
            'customers': employee_customers
        }
        return render(request, 'employees/filter_pickups.html', context)

