import main.views
from . import views
from django.urls import path

# import activity.views



#Views
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard-page'),
    path('dashboard/lectures' , views.dashboard_lectures , name="dashboard-lectures"),
    path('dashboard/lecture/<slug:slug>' , views.dashboard_lecture , name="lesson-page"),

    path('dashboard/chapters' , views.dashboard_chapters , name="dashboard-chapters"),
    path('dashboard/chapters/<slug:slug>' , views.dashboard_chapter_details , name="chapter-details"),

    path('dashboard/groups' , views.dashboard_groups , name="dashboard-groups"),
    path('dashboard/groups/<slug:slug>' , views.dashboard_group_details , name="group-details"),

    path('dashboard/upload' , views.dashboard_upload , name="dashboard-upload-page"),
    path('dashboard/assignments' , views.dashboard_assignments , name="dashboard-assignments"),
    path('dashboard/codes' , views.dashboard_codes , name="dashboard-codes"),
    path('dashboard/questions' , views.dashboard_questions , name="dashboard-questions"),
    path('dashboard/sales' , views.dashboard_sales , name="dashboard-sales"),
    path('dashboard/students' , views.dashboard_students , name="dashboard-students"),
    path('dashboard/themes' , views.dashboard_themes , name="dashboard-themes"),


    path('groups/invite' , views.invite_group , name="invite-group"),

    path('wallet/recharge', views.charge_wallet_code, name='wallet-recharge-code'),
    path('wallet/requests', views.wallet_requests, name='wallet-requests'),

    path('wallet/code-charge/request', views.code_charge, name='code-recharge'),

    path('purchase-error', views.money_error, name='money-error'),

    # path('wallet/statement', main.views.account_activity, name='account-activity'),
    # path('wallet/payments', main.views.account_payment, name='account-payment'),
    # path('student/results', main.views.account_results, name='student-results'),
]



