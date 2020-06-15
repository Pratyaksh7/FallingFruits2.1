from django.urls import path
from ecommerce import views

urlpatterns = [
    path('sample/',views.sample, name='sample'),
    path('upload-csv/',views.location_upload, name='location_upload'),
    path('',views.dashboard,name='dashboard'),
    path('cart/',views.cart, name='cart'),
    path('cart/checkout/',views.checkout,name='checkout'),
    path('map/',views.maps, name='map'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
]
