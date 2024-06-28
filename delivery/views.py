from django.shortcuts import render, redirect
from .forms import ReviewsForm
from .models import Reviews, DeliveryOrder
from customers.models import Customer
from django.contrib import messages
from customers.forms import OrderTrackingForm
from django.views.generic import DetailView
import folium
#Create your views here.

def home(request):
    if request.method == 'POST':
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            tracking_number = form.cleaned_data.get('tracking_number')
            request.session['tracking_number'] = tracking_number
            order = DeliveryOrder.objects.filter(tracking_number=tracking_number).first()
            if order:
                return render(request, 'delivery/deliveryorder_detail.html', {'order':order})
            else:
                messages.error(request, f'There is no order with {tracking_number}')
    else:
        form = OrderTrackingForm()
    context = {'form':form}
    return render(request, 'delivery/home.html', context=context)

def about(request):
    # customer = Customer.objects.filter(email='sharpdelivery616@gmail.com').first()
    # customer.is_staff = True
    # customer.is_superuser = True
    # customer.save()
    return render(request, 'delivery/about.html')

def service(request):
    # user = Customer.objects.filter(email='ehirimchiedozie96@yahoo.com').first()
    # user.delete()
    return render(request, 'delivery/service.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_host(request):
    host_name = request.META.get('REMOTE_HOST')
    return host_name

def contact(request):
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            ip_address = get_client_ip(request)
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            sender = Reviews(name=name, email=email, subject=subject, message=message, ip_address=ip_address)
            sender.save()
            messages.success(request, 'Your review has been submitted successfully.')
            
    else:
        form = ReviewsForm()
    context = {'form' : form}
    return render(request, 'delivery/contact.html')

def price(request):
    return render(request, 'delivery/price.html')

def single(request):
    return render(request, 'delivery/single.html')


class OrderDetailView(DetailView):
    model = DeliveryOrder
    context_object_name = 'order'
    template_name = 'delivery/deliveryorder_detail.html'


def map_view(request):
    cordinates = [6.9244, 3.3792]
    m = folium.Map(location=cordinates, zoom_start=13)
    folium.Marker(cordinates, popup='My point').add_to(m)
    map_html = m._repr_html_()
    context = {
        'map': map_html,
    }
    return render(request, 'customers/map.html', context)