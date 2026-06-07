from django.urls import path
from . import views

urlpatterns = [
    path('danh-gia/', views.review_create_view, name='review_create'),
]