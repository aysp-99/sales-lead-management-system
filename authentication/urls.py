from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.user_registration, name='user_registration'),
    path('logout/', views.logout_view, name='logout'),
]
