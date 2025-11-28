from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:news_pk>/', views.news_detail, name='news_detail'),
    path('<int:news_pk>/bookmark/', views.news_bookmark, name='news_bookmark'),
]
