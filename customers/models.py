from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomerManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, phonenumber, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        if not password:
            raise ValueError('Password is not provided')
        
        customer = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phonenumber=phonenumber,
            **extra_fields
        )

        customer.set_password(password)
        customer.save(using=self._db)
        return customer
    
    def create_user(self, email, password=None, first_name='', last_name='', phonenumber='', **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, phonenumber, **extra_fields)
    
    def create_superuser(self, email, password=None, first_name='', last_name='', phonenumber='', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, phonenumber, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=200)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    phonenumber = models.CharField(unique=True, max_length=100, blank=True, null=True, default='')
    ip_address = models.GenericIPAddressField(default='127.0.0.1')
    date_registered = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phonenumber']

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

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
    tracking_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'Order {self.id} - {self.status}'

class OrderTracking(models.Model):
    order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='trackings')
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tracking {self.id} for Order {self.order.id}'
