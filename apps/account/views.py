from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from apps.bookings.models import Booking
from django.contrib import messages
from django.utils import timezone


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        phone    = request.POST.get('phone', '')
        address  = request.POST.get('address', '')

        # Kiểm tra tài khoản đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            error = 'Tên đăng nhập đã tồn tại.'
        elif User.objects.filter(email=email).exists():
            error = 'Email đã được sử dụng.'
        else:
            # Tạo User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Tạo CustomerProfile
            CustomerProfile.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            # Đăng nhập luôn sau khi đăng ký
            login(request, user)
            return redirect('home')

    return render(request, 'account/register.html', {'error': error})


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Admin → dashboard, khách hàng → trang chủ
            if user.is_staff:
                return redirect('dashboard')
            return redirect('home')
        error = 'Sai tên đăng nhập hoặc mật khẩu.'
    return render(request, 'account/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    profile = CustomerProfile.objects.get(user=request.user)
    success = False
    
    if request.method == 'POST':
        profile.phone   = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        success = True
        
    my_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'account/profile.html', {
    'profile':  profile,
    'bookings': Booking.objects.filter(user=request.user).order_by('-created_at'),
    'success':  success,
    'today':    timezone.now().date(),
})




def huy_don(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        today = timezone.now().date()
        
        # Chỉ cho huỷ nếu còn trước 1 ngày
        if booking.booking_date <= today:
            messages.error(request, 
                f'Không thể huỷ đơn #{booking.id}. Chỉ được huỷ trước ngày thực hiện ít nhất 1 ngày.')
        elif booking.status in ['cancelled', 'done']:
            messages.error(request, 
                f'Đơn #{booking.id} không thể huỷ do đã {booking.get_status_display()}.')
        else:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 
                f'Huỷ đơn #{booking.id} thành công!')
    
    return redirect('profile')
