from django.urls import path
from . import views

# Views 
urlpatterns = [
    path('profile/<str:pk>', views.main, name='main'),

    path('profile/<str:pk>/wallet/recharge', views.wallet_recharge, name='wallet-recharge'),
    path('profile/<str:pk>/wallet/subscriptions', views.wallet_subscriptions, name='wallet-subscriptions'),
    path('profile/<str:pk>/wallet/transactions', views.wallet_transactions, name='wallet-transactions'),

    path('profile/<str:pk>/groups', views.groups, name='groups'),
    path('profile/<str:pk>/group/<str:gr>', views.group, name='group'),
    path('group/join/<str:group_link>', views.group_join_link, name='group-join-link'),

    path('profile/<str:pk>/account', views.account, name='account'),
    path('profile/<str:pk>/account/connections', views.connections, name='account-connections'),
    path('profile/<str:pk>/account/login-history', views.login_history, name='account-login-history'),

    path('profile/<str:pk>/notifications', views.notifications, name='notifications'),
    path('profile/<str:pk>/inbox', views.inbox, name='inbox'),


    path('profile/<str:pk>/lectures', views.lectures, name='lectures'),
    path('profile/<str:pk>/homeworks', views.homeworks, name='homeworks'),
    path('profile/<str:pk>/exams', views.exams, name='exams'),
    path('profile/<str:pk>/statistics', views.statistics, name='statistics'),
]


