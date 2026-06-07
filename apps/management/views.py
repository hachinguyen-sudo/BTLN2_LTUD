from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from apps.bookings.models import Booking, Payment
from apps.services.models import Service
from apps.reviews.models import Review
from django.contrib import messages
from apps.bookings.models import Promotion



def staff_required(view_func):
    """Decorator kiểm tra quyền admin (is_staff)"""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def dashboard_view(request):
    today = timezone.now().date()

    stats = {
        'tong_booking':    Booking.objects.count(),
        'cho_xac_nhan':    Booking.objects.filter(status='pending').count(),
        'hom_nay':         Booking.objects.filter(booking_date=today).count(),
        'hoan_thanh':      Booking.objects.filter(status='done').count(),
        'tong_doanh_thu':  sum(
            p.amount for p in Payment.objects.filter(status='success')
        ),
    }
    booking_moi = Booking.objects.order_by('-created_at')[:10]
    return render(request, 'management/dashboard.html', { 
        'stats':       stats,
        'booking_moi': booking_moi,
    })

@staff_required
def manage_orders_view(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related(
        'user', 'service', 'promotion'
    ).order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'management/bookings.html', {
        'bookings':      bookings,
        'status_filter': status_filter,
    })


@staff_required
def update_order_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled', 'done']:
            booking.status = new_status
            booking.save()
    return redirect('manage_orders')


@staff_required
def manage_services_view(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'management/services.html', {'services': services})


@staff_required
def toggle_service_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.is_active = not service.is_active
    service.save()
    return redirect('manage_services')


@staff_required
def manage_users_view(request):
    users = User.objects.filter(is_staff=False).select_related('customerprofile')
    return render(request, 'management/users.html', {'users': users})


@staff_required
def manage_reviews_view(request):
    reviews = Review.objects.select_related(
        'booking', 'booking__user'
    ).order_by('-created_at')
    return render(request, 'management/reviews.html', {'reviews': reviews})


@staff_required
def toggle_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_visible = not review.is_visible
    review.save()
    return redirect('manage_reviews')



@staff_required
def them_dich_vu(request):
    error = None
    if request.method == 'POST':
        name           = request.POST.get('name')
        description    = request.POST.get('description')
        price          = request.POST.get('price')
        duration_hours = request.POST.get('duration_hours')
        image          = request.FILES.get('image')

        try:
            service = Service.objects.create(
                name=name,
                description=description,
                price=price,
                duration_hours=duration_hours,
                is_active=True
            )
            if image:
                service.image = image
                service.save()
            messages.success(request, f'Thêm dịch vụ "{name}" thành công!')
            return redirect('manage_services')
        except Exception as e:
            error = f'Lỗi: {str(e)}'

    return render(request, 'management/them_dich_vu.html', {'error': error})


@staff_required
def sua_dich_vu(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    error   = None

    if request.method == 'POST':
        service.name           = request.POST.get('name')
        service.description    = request.POST.get('description')
        service.price          = request.POST.get('price')
        service.duration_hours = request.POST.get('duration_hours')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')
        try:
            service.save()
            messages.success(request, f'Cập nhật dịch vụ "{service.name}" thành công!')
            return redirect('manage_services')
        except Exception as e:
            error = f'Lỗi: {str(e)}'

    return render(request, 'management/sua_dich_vu.html', {
        'service': service,
        'error':   error,
    })


@staff_required
def xoa_dich_vu(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        ten = service.name
        service.delete()
        messages.success(request, f'Đã xoá dịch vụ "{ten}"!')
    return redirect('manage_services')

@staff_required
def quan_ly_khuyen_mai(request):
    promotions = Promotion.objects.all().order_by('-id')
    return render(request, 'management/quan_ly_khuyen_mai.html', {'promotions': promotions})

@staff_required
def them_khuyen_mai(request):
    if request.method == 'POST':
        code = request.POST.get('code').upper().strip()
        description = request.POST.get('description') # Bổ sung dòng này
        discount_percent = request.POST.get('discount_percent')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_active = request.POST.get('is_active') == 'on'

        Promotion.objects.create(
            code=code, description=description, discount_percent=discount_percent,
            start_date=start_date, end_date=end_date, is_active=is_active
        )
        messages.success(request, f'Đã thêm mã {code} thành công!')
        return redirect('quan_ly_khuyen_mai')
    
    return render(request, 'management/them_khuyen_mai.html')

@staff_required
def sua_khuyen_mai(request, promo_id):
    promo = get_object_or_404(Promotion, id=promo_id)
    if request.method == 'POST':
        promo.code = request.POST.get('code').upper().strip()
        promo.description = request.POST.get('description') # Bổ sung dòng này
        promo.discount_percent = request.POST.get('discount_percent')
        promo.start_date = request.POST.get('start_date')
        promo.end_date = request.POST.get('end_date')
        promo.is_active = request.POST.get('is_active') == 'on'
        promo.save()
        messages.success(request, f'Đã cập nhật mã {promo.code}!')
        return redirect('quan_ly_khuyen_mai')
        
    return render(request, 'management/sua_khuyen_mai.html', {'promo': promo})
@staff_required
def xoa_khuyen_mai(request, promo_id):
    promo = get_object_or_404(Promotion, id=promo_id)
    if request.method == 'POST':
        promo.delete()
        messages.success(request, 'Đã xoá mã khuyến mãi!')
    return redirect('quan_ly_khuyen_mai')



