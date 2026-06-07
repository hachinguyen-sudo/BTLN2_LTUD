from django.shortcuts import render, get_object_or_404
from .models import Service
from apps.reviews.models import Review

def home_view(request):
    services = Service.objects.filter(is_active=True).order_by('-created_at')[:3]
    danh_gia = Review.objects.filter(is_visible=True).order_by('-created_at')[:6]  
    return render(request, 'services/home.html', {
        'services': services,
        'danh_gia': danh_gia,
    })

def service_list_view(request):
    query = request.GET.get('q')
    services = Service.objects.filter(is_active=True)
    if query:
        services = services.filter(name__icontains=query)
        
    return render(request, 'services/services.html', {
        'services': services,
        'query': query 
    })


def service_detail_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    return render(request, 'services/services-detail.html', {'service': service})

