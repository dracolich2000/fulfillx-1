from django.db import models

# Create your models here.

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255, null=True,blank=True)
    shop_url = models.URLField(unique=True)
    access_token = models.TextField()
    shop_platform = models.CharField(max_length=50, default='Shopify')
    linked_by = models.CharField(max_length=255,null=True, blank=True)
    linked_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)

class ShopifyOrder(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    payment_status = models.CharField(max_length=255, blank=True, null=True)
    fulfillment_status = models.CharField(max_length=255, blank=True, null=True)
    delivery_status = models.CharField(max_length=255, blank=True, null=True)

class ShopifyOrderItem(models.Model):
    order = models.ForeignKey(ShopifyOrder, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of individual item
