from django.urls import path, include
from django.contrib import admin
from . import views

app_name = "feed"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_req, name='login'),
    path('logout/', views.logout_req, name='logout'),
    path('register/', views.register, name='register'),
    path('<str:profile>/', views.profile, name='profile'),
    path('admin', admin.site.urls),
]