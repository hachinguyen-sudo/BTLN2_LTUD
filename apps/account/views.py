from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile


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
    return render(request, 'account/profile.html', {
        'profile': profile,
        'success': success,
    })
