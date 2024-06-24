from django.shortcuts import render
# from .forms import ReviewsForm
# from .models import Reviews
# from customers.models import Customer
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'delivery/home.html')

def about(request):
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
    # if request.method == 'POST':
    #     form = ReviewsForm(request.POST)
    #     if form.is_valid():
    #         ip_address = get_client_ip(request)
    #         name = form.cleaned_data.get('name')
    #         email = form.cleaned_data.get('email')
    #         subject = form.cleaned_data.get('subject')
    #         message = form.cleaned_data.get('message')
    #         sender = Reviews(name=name, email=email, subject=subject, message=message, ip_address=ip_address)
    #         sender.save()
    #         messages.success(request, 'Your review has been submitted successfully.')
            
    # else:
    #     form = ReviewsForm()
    # context = {'form' : form}
    return render(request, 'delivery/contact.html')

def price(request):
    return render(request, 'delivery/price.html')

def single(request):
    return render(request, 'delivery/single.html')


