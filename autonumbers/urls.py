from django.urls import path
from . import views_auth, views_main, views_admin
from .views_main import logout_view

urlpatterns = [
    path('', views_main.home_page, name='home'),

    path('login/', views_auth.user_login, name='login'),
    path('register/', views_auth.user_register, name='register'),
    path("logout/", logout_view, name="logout"),

    path('profile/', views_auth.profile_page, name='profile_page'),

    path('subscribe/', views_main.subscribe_search, name='subscribe_search'),
    path('unsubscribe/<int:pk>/', views_main.cancel_subscription, name='cancel_subscription'),

    path('create/', views_main.create_search, name='create_search'),
    path('my-searches/', views_main.my_searches, name='my_searches'),
    path("ajax/load-tscs/", views_main.load_tscs, name="ajax_load_tscs"),
    path('success/', views_main.search_success, name='search_success'),

    path("admin-panel/", views_admin.admin_subscriptions_view, name="admin_subscriptions"),
]