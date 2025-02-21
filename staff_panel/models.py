from django.db import models
from authentication.models import StaffUser

# Create your models here.
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    images = models.ManyToManyField('ProductImage', related_name='products')
    category = models.CharField(max_length=255, default='')
    description = models.TextField()
    inventory = models.PositiveIntegerField(default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")

class ProductImage(models.Model):
    image_url = models.URLField(max_length=255, blank=False, default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg')

class SourcingProductRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=500)
    image = models.ImageField(upload_to='sourcing_products/')
    description = models.TextField()
    added_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    review = models.TextField(blank=True, null=True)