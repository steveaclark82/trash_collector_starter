from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('register_customer/', views.create_customer, name='register_customer'),
    path('set_pickup/', views.weekly_pickup, name="set_pickup"),
    path('pickup_suspension/', views.suspend_pickup, name="pickup_suspension"),
    path('account_info/', views.account_info, name="account_info"),
    path('onetime_pickup/', views.onetime_pickup, name="onetime_pickup")
]