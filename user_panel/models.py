from django.db import models

# store products pushed to shopify
class MyProducts(models.Model):
    product = models.OneToOneField('staff_panel.Products', on_delete=models.CASCADE, primary_key=True)
    fulfillx_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)
    shopify_product_id = models.CharField(max_length=255, blank=True, null=True)
    pushed_to_shopify = models.BooleanField(default=False)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, blank=True,null=True)
    vendor = models.ForeignKey('authentication.StaffUser', on_delete=models.SET_NULL, null=True, blank=True, related_name="myProducts")

# store shop data
class Shop(models.Model): 
    id = models.AutoField(primary_key=True)
    shop_name = models.CharField(max_length=255, null=True,blank=True)
    shop_url = models.URLField(unique=True)
    access_token = models.TextField()
    shop_platform = models.CharField(max_length=50, default='Shopify')
    linked_by = models.CharField(max_length=255,null=True, blank=True)
    linked_on = models.DateTimeField(auto_now_add=True, null=True,blank=True)

# store orders
class ShopifyOrder(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    payment_status = models.CharField(max_length=255, blank=True, null=True)
    fulfillment_status = models.CharField(max_length=255, blank=True, null=True)
    delivery_status = models.CharField(max_length=255, blank=True, null=True)
    shop = models.ForeignKey('Shop', on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)

# store order items
class ShopifyOrderItem(models.Model):
    order = models.ForeignKey(ShopifyOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(MyProducts, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)  # Store name to keep history
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

