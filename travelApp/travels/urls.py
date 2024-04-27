from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('tours/', views.index, name='list'),
    path('tours/<int:tour_id>', views.list, name='list'),
    path('category/', views.CategoryView.as_view())
]
