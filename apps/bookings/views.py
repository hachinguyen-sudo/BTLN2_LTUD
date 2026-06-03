from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking, Payment, Promotion
from apps.services.models import Service

# Danh sách quận nội thành phục vụ
QUAN_NOI_THANH = [
    'Hoàn Kiếm', 'Đống Đa', 'Hai Bà Trưng', 'Ba Đình',
    'Tây Hồ', 'Cầu Giấy', 'Thanh Xuân', 'Hoàng Mai', 'Long Biên',
]


@login_required(login_url='login')
def booking_create_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    error   = None

    if request.method == 'POST':
        district     = request.POST.get('district')
        booking_date = request.POST.get('booking_date')
        time_slot    = request.POST.get('time_slot')
        address      = request.POST.get('address')
        note         = request.POST.get('note', '')
        promo_code   = request.POST.get('promotion_code', '').strip()

        # Bước 1: Kiểm tra vùng phục vụ
        if district not in QUAN_NOI_THANH:
            error = 'Khu vực chưa được hỗ trợ. Chúng tôi phục vụ nội thành Hà Nội.'

        else:
            # Bước 2: Kiểm tra overbooking
            so_lich = Booking.objects.filter(
                booking_date=booking_date,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).count()

            if so_lich >= 3:
                error = 'Khung giờ này đã kín lịch. Vui lòng chọn giờ khác.'
            else:
                # Bước 3: Kiểm tra mã khuyến mãi
                promotion = None
                if promo_code:
                    today = timezone.now().date()
                    try:
                        promotion = Promotion.objects.get(
                            code=promo_code,
                            is_active=True,
                            start_date__lte=today,
                            end_date__gte=today
                        )
                    except Promotion.DoesNotExist:
                        error = 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn.'

                if not error:
                    # Bước 4: Tính tiền
                    if promotion:
                        total = service.price * (1 - promotion.discount_percent / 100)
                    else:
                        total = service.price

                    # Bước 5: Tạo Booking
                    booking = Booking.objects.create(
                        user=request.user,
                        service=service,
                        promotion=promotion,
                        address=address,
                        district=district,
                        booking_date=booking_date,
                        time_slot=time_slot,
                        note=note,
                        total_amount=total,
                        status='pending'
                    )
                    return redirect('payment_checkout', booking_id=booking.id)

    return render(request, 'bookings/booking-form.html', {
        'service':   service,
        'quan_list': QUAN_NOI_THANH,
        'error':     error,
    })


@login_required(login_url='login')
def payment_checkout_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('method')
        Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            method=method,
            status='success',
        )
        booking.status = 'confirmed'
        booking.save()
        return redirect('payment_success', booking_id=booking.id)

    return render(request, 'bookings/payment.html', {'booking': booking})


@login_required(login_url='login')
def payment_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment = Payment.objects.get(booking=booking)
    return render(request, 'bookings/payment-success.html', {
        'booking': booking,
        'payment': payment,
    })


def search_order_view(request):
    booking = None
    error   = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '').strip()
        phone    = request.POST.get('phone', '').strip()
        try:
            booking = Booking.objects.get(
                id=order_id,
                user__customerprofile__phone=phone
            )
        except Booking.DoesNotExist:
            error = 'Không tìm thấy đơn hàng. Vui lòng kiểm tra lại.'
    return render(request, 'bookings/search-order.html', {
        'booking': booking,
        'error':   error,
    })