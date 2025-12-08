from django.db import models
from django.conrib.auth.models import User

class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('B','Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),    
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')

    class Meta:
        ordering = ['user__username']
        indexes = [
            models.Index(fields=['user__last_name', 'user__first_name'])
        ]

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # product_set 자동생성

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # prevent circular import by using string 'Product' and related_name='+'
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    
    title= models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    description = models.TextField()
    # 666666.22
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)    
    inventory = models.PositiveSmallIntegerField()
    # 최종 업데이트한 시점(auto_now: 한번정하변 안변함)
    last_update = models.DateTimeField(auto_now_add=True)
    # orderitem 자동생성
    
    def __str__(self) -> str:
        return self.title

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    PAYMENT_STATUS_CHOICES = [
        ('P','Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),    
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='P')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)

class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.city}'

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'CartItem: {self.product.title} (x{self.quantity}) in Cart {self.cart.id}' # type: ignore