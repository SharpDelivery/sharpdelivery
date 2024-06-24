from django.shortcuts import render, get_object_or_404
from .models import Customer, DeliveryOrder, OrderTracking
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .forms import AccountOpeningForm, OrderTrackingForm, CustomerUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def register(request):
    if request.method == 'POST':
        form = AccountOpeningForm(request.POST)
        if form.is_valid():
            form.save()
            customer = Customer.objects.get(phonenumber=form.cleaned_data.get('phonenumber'))
            customer.ip_address = get_client_ip(request)
            customer.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            messages.success(request, f'Account created for {first_name} {last_name} was successful')
            return redirect('home')
    else:
        form = AccountOpeningForm()
    return render(request, 'customers/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            tracking_number = form.cleaned_data.get('tracking_number')
            order = DeliveryOrder.objects.filter(tracking_number=tracking_number).first()
            if order:
                messages.success(request, f'Your order with tracking number {tracking_number} is {order.status}')
            else:
                messages.info(request, f'There is no order with tracking number {tracking_number}')
    else:
        form = OrderTrackingForm()
    return render(request, 'customers/profile.html', {'form':form}) 

@login_required
def update_account(request):
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account informations has been successfully updated')
    else:
        form = CustomerUpdateForm(instance=request.user)
    return render(request, 'customers/update_account.html', {'form':form})

@login_required
def confirm_logout(request):
    return render(request, 'customers/confirm_logout.html')

def order_list(request):
    orders = DeliveryOrder.objects.all()
    return render(request, 'customers/order_list.html', {'orders': orders})

class OrderListView(ListView, LoginRequiredMixin):
    models = DeliveryOrder
    context_object_name = 'orders'
    template_name = 'customers/order_list.html'

    def get_queryset(self):
        return DeliveryOrder.objects.all()

def order_detail(request, order_id):
    order = get_object_or_404(DeliveryOrder, id=order_id)
    tracking_info = OrderTracking.objects.filter(order=order)
    return render(request, 'customers/order_detail.html', {'order': order, 'tracking_info': tracking_info})

def track_order(request, tracking_number):
    order = get_object_or_404(DeliveryOrder, tracking_number=tracking_number)
    tracking_info = OrderTracking.objects.filter(order=order)
    tracking_data = [{'status': t.status, 'location': t.location, 'timestamp': t.timestamp} for t in tracking_info]
    return JsonResponse({'order': order.id, 'tracking_number': order.tracking_number, 'status': order.status, 'tracking_info': tracking_data})


class OrderListView(ListView, LoginRequiredMixin):
    models = DeliveryOrder
    context_object_name = 'orders'
    template_name = 'customers/order_list.html'

    def get_queryset(self):
        return DeliveryOrder.objects.filter(customer=self.request.user).all()