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
]