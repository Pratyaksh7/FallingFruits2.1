from django.urls import path
from . import views

urlpatterns = [
    path('',views.Overview, name='overview'),
    path('location-list/', views.LocationList, name='location-list'),
    path('location-detail/<str:pk>/', views.LocationDetail, name='location-detail'),
    path('location-create/', views.LocationCreate, name='location-create'),
    path('location-update/<str:pk>/', views.LocationUpdate, name='location-update'),
    path('location-delete/<str:pk>/', views.LocationDelete, name='location-delete'),
]
