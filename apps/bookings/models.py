from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Service

class Promotion(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    discount_percent = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'), ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy'), ('done', 'Hoàn thành'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    district = models.CharField(max_length=50)
    booking_date = models.DateField()
    time_slot = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=(('cash', 'Tiền mặt'), ('bank_transfer', 'Chuyển khoản')))
    status = models.CharField(max_length=10, default='success')
    paid_at = models.DateTimeField(auto_now_add=True)
    