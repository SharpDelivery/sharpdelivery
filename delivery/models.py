from django.db import models
from customers.models import Customer
from django.urls import reverse
# Create your models here.

class Reviews(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=500)
    message = models.TextField()

class DeliveryOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    deliver_to = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return f'Order {self.tracking_number} - {self.status}'
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk' : self.pk})
    