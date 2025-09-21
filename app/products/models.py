import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    ssn = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class ProductChangeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='change_logs')
    action = models.CharField(max_length=20)
    changed_fields = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} - {self.action}"