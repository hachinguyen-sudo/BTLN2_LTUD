from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',
         views.dashboard_view, name='dashboard'),
    path('don-hang/',
         views.manage_orders_view, name='manage_orders'),
    path('don-hang/cap-nhat/<int:booking_id>/',
         views.update_order_status_view, name='update_order_status'),
    path('dich-vu/',
         views.manage_services_view, name='manage_services'),
    path('dich-vu/an-hien/<int:service_id>/',
         views.toggle_service_view, name='toggle_service'),
    path('nguoi-dung/',
         views.manage_users_view, name='manage_users'),
    path('danh-gia/',
         views.manage_reviews_view, name='manage_reviews'),
    path('danh-gia/an-hien/<int:review_id>/',
         views.toggle_review_view, name='toggle_review'),
     path('dich-vu/them/',              views.them_dich_vu,  name='them_dich_vu'),
     path('dich-vu/sua/<int:service_id>/', views.sua_dich_vu, name='sua_dich_vu'),
     path('dich-vu/xoa/<int:service_id>/', views.xoa_dich_vu, name='xoa_dich_vu'),
     path('khuyen-mai/', views.quan_ly_khuyen_mai, name='quan_ly_khuyen_mai'),
     path('khuyen-mai/them/', views.them_khuyen_mai, name='them_khuyen_mai'),
     path('khuyen-mai/sua/<int:promo_id>/', views.sua_khuyen_mai, name='sua_khuyen_mai'),
     path('khuyen-mai/xoa/<int:promo_id>/', views.xoa_khuyen_mai, name='xoa_khuyen_mai'),
]