from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Review
from apps.bookings.models import Booking


@login_required(login_url='login')
def review_create_view(request):
    error   = None
    success = False

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(
                id=booking_id,
                user=request.user,
                status='done'
            )
            if hasattr(booking, 'review'):
                error = 'Đơn hàng này đã được đánh giá rồi.'
            else:
                Review.objects.create(
                    booking=booking,
                    rating=request.POST.get('rating'),
                    comment=request.POST.get('comment', ''),
                )
                success = True
        except Booking.DoesNotExist:
            error = 'Không tìm thấy đơn hàng đã hoàn thành.'

    # Lấy danh sách đơn đã done của user để chọn đánh giá
    done_bookings = Booking.objects.filter(
        user=request.user,
        status='done'
    ).exclude(review__isnull=False)

    return render(request, 'reviews/review.html', {
        'error':         error,
        'success':       success,
        'done_bookings': done_bookings,
    })

