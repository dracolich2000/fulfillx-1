from django.shortcuts import render, redirect, get_object_or_404
from staff_panel.models import Products
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from fulfillX.access_control_decorater import role_required
from user_panel.models import ShopifyOrder, MyProducts
from authentication.models import StaffUser

# Create your views here.
@role_required('Vendor')
@login_required(login_url='login')
@never_cache
def vendor_dashboard(request):
    return render(request, 'vendor_panel/dashboard.html')

@role_required('Vendor')
@login_required(login_url='login')
@never_cache
def products(request):
    vendor = StaffUser.objects.get(username=request.user.username)
    products = Products.objects.filter(vendor=vendor)
    return render(request, 'vendor_panel/products.html',{'products':products})

@role_required('Vendor')
@login_required(login_url='login')
@never_cache
def update_inventory(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        inventory = request.POST.get('product_inventory')
        
        try:
            product = get_object_or_404(Products, id=product_id)
            product.inventory = inventory
            product.save()
        
            messages.success(request, 'Inventory updated successfully!')
            return redirect('vendor_products')
        except:
            messages.error(request, 'Please try again!')
            return redirect('vendor_products')

@role_required('Vendor')
@login_required(login_url='login')
@never_cache
def orders(request):
    vendor = StaffUser.objects.get(username=request.user.username)
    products = MyProducts.objects.filter(vendor=vendor)
    orders = ShopifyOrder.objects.filter(items__product__in=products)
    return render(request, 'vendor_panel/orders.html',{'orders':orders})