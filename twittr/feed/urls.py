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
    path('delete/<int:tweet_pk>/<str:redirect_url>/', views.tweet_delete, name='tweet_delete'),
    path('delete_reply/<int:reply_pk>/<int:tweet_pk>/<str:redirect_url>/', views.reply_delete, name='reply_delete'),
    path('search/<str:search_term>/', views.search, name='search'),
    path('<str:profile>/following/', views.following, name='following'),
    path('<str:profile>/followers/', views.followers, name='followers'),
    path('admin', admin.site.urls),
]