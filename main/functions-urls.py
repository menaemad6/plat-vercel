from django.urls import path
from . import views

# Views 
urlpatterns = [
    path('logout', views.logout, name='logout'),




    path('join-lecture', views.lecture_code_join_function, name='join-lecture'),
    path('purchase-lecture', views.purchase_lecture, name='purchase-lecture'),
    path('discounts-functions', views.discounts_functions, name='discounts-functions'),




]


