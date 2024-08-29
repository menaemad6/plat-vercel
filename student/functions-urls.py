from django.urls import path
from . import views

# Views 
urlpatterns = [
    path('wallet-recharge', views.code_charge_function, name='wallet-recharge'),
    path('vodafone-recharge', views.vodaphone_charge_function, name='vodaphone-recharge'),

    path('questions-functions', views.questions_functions, name='questions-functions'),


    path('delete-notification', views.delete_notification, name='delete-notification'),
]


