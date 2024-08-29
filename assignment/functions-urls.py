import main.views
from . import views
from django.urls import path



#Functions
urlpatterns = [
    path('create-assignment' , views.create_assignment , name="create-assignment"),

    path('assignment-functions' , views.assignment_functions , name="assignment-functions"),
]



