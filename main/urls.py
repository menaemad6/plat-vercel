from django.urls import path
from . import views

from assignment import views as assignment_views
# Views 
urlpatterns = [
    path('testing', views.testing_page, name='testing'),

    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),




    path('lectures', views.grades, name='grades'),
    path('lectures/<str:grade>', views.grade, name='grade'),

    path('lecture/<str:id>', views.lecture, name='lecture'),
    path('lecture/<str:id>/video/<str:video>', views.lecture_video, name='lecture-video'),
    path('lecture/<str:id>/attachment/<str:attachment>', views.lecture_attachment, name='lecture-attachment'),
    path('lecture/<str:id>/assignment/<str:assignment>', assignment_views.lecture_assignment , name='lecture-assignment'),


    path('lecture/<str:id>/code/<str:lecture_code>', views.lecture_code_students, name='lecture-code-students'),
    path('lecture/<str:id>/join/<str:lecture_code>', views.lecture_code_join, name='lecture-code-join'),

    path('questions', views.grades, name='questions'),

]


