from django.urls import path
from . import views

urlpatterns = [
    path('dat-lich/<int:service_id>/', views.booking_create_view, name='booking_create'),
    path('thanh-toan-thanh-cong/<int:booking_id>/', views.payment_success_view, name='payment_success'),
    path('kiem-tra-ma/', views.kiem_tra_ma_view, name='kiem_tra_ma'),
]