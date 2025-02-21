from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Products, ProductImage, SourcingProductRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import csv
from django.conf import settings
from authentication.models import StaffUser
from fulfillX.access_control_decorater import role_required
import logging
from decimal import Decimal
from user_panel.models import Shop, ShopifyOrder, ShopifyOrderItem, MyProducts
import requests

# Create your views here.
@role_required('Staff')
@login_required(login_url='login')
@never_cache
def staff_dashboard(request):
    return render(request, 'staff_panel/dashboard.html')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def products(request):
    products = Products.objects.all()
    vendors = StaffUser.objects.filter(role='Vendor')
    return render(request, 'staff_panel/products.html',{'products':products,
                                                  'vendors':vendors})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def add_product(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['product_description']
        image_urls = request.POST['image_urls']
        vendor = request.POST['vendor']
        category = request.POST['category']

        try:
            product = Products.objects.create(
                name=name,
                price=price,
                category=category,
                description=description,
                created_by=request.user.username,
                vendor = vendor
            )
            
            urls_list = image_urls.replace('\n', ',').replace(' ', ',').split(',')
            urls_list = [url.strip() for url in urls_list if url.strip()]
            
            images = []
            for url in urls_list:
                image = ProductImage.objects.create(image_url=url)
                images.append(image)

            product.images.add(*images)

            messages.success(request, 'Product added Successfully!')
            return redirect('staff_products')
        
        except Exception as e:
            logging.error(f'error occured!:{str(e)}')
            messages.error(request, 'Something went wrong. Please try again!')
            return redirect('staff_products')
        
@role_required('Staff')
@login_required(login_url='login')
@never_cache
def upload_products_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('staff_products')

        file_data = csv_file.read().decode('utf-8')
        csv_data = csv.reader(file_data.splitlines())
        try:
            next(csv_data)
            for line_number, row in enumerate(csv_data, start=1):
                if len(row) != 6:
                    messages.error(request, f"Invalid row format line [{line_number}]: {row}. It must have 6 columns.")
                    return redirect('staff_products')
                
                name, price, category, description, vendor_username, image_urls = row
                
                try:
                    vendor = StaffUser.objects.get(username=vendor_username,role='Vendor')
                except StaffUser.DoesNotExist:
                    messages.error(request,f'Line {line_number}: Vendor "{vendor_username}" does not exist. Please check your file and try again.')
                    redirect('staff_products')

                try:
                    price = Decimal(price.strip())  # Ensure it's a valid decimal
                except ValueError:
                    messages.error(request, f'Error on line {line_number}: Price "{price}" is not a valid decimal number.')
                    return redirect('staff_products')

                if vendor:
                    product = Products.objects.create(
                        name=name,
                        price=price,
                        category=category,
                        description=description,
                        vendor=vendor,
                        created_by=request.user.username
                    )
                    urls_list = image_urls.replace('|', ',').replace(' ', ',').split(',')
                    urls_list = [url.strip() for url in urls_list if url.strip()]

                    images = []
                    for url in urls_list:
                        image= ProductImage.objects.create(image_url=url)
                        images.append(image)
                    product.images.add(*images)

            messages.success(request, 'Products uploaded successfully.')
        except Exception as e:
            logging.error(f'Error occured:{str(e)}')
            messages.error(request,'Something went wrong! Please try again.')
        return redirect('staff_products')


@role_required('Staff')
@login_required(login_url='login')
@never_cache
def update_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    vendors = StaffUser.objects.filter(role='Vendor')

    if request.method == "POST":
        # Update product details
        product.name = request.POST.get("name")
        product.price = request.POST.get('price')
        product.description = request.POST.get("description")
        product.inventory = request.POST.get("inventory")
        product.category = request.POST.get('category')
        product.save()

        # Delete selected images
        delete_images = request.POST.getlist('delete_images')
        print(delete_images)
        ProductImage.objects.filter(id__in=delete_images).delete()

        # Add new images
        new_image_urls = request.POST['new_image_urls']

        urls_list = new_image_urls.replace('\n', ',').replace(' ', ',').split(',')
        urls_list = [url.strip() for url in urls_list if url.strip()]

        images = []
        for url in urls_list:
            image = ProductImage.objects.create(image_url=url)
            images.append(image)

        product.images.add(*images)

        messages.success(request, "Product updated successfully!")
        return HttpResponseRedirect('/staff_products/#existing-products')

    return render(request, "staff_panel/update_product.html", {"product": product,
                                                         'vendors':vendors})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def delete_product(request, product_id):
    product = get_object_or_404(Products,id=product_id)
    
    product.images.all().delete()
    # Delete the product
    product.delete()

    messages.success(request, "Product and associated images deleted successfully.")
    return redirect('staff_products')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def sourcing_requests(request):
    completed_requests = SourcingProductRequest.objects.filter(status='Completed')
    pending_requests = SourcingProductRequest.objects.filter(status='Pending')
    in_progress_requests = SourcingProductRequest.objects.filter(status='In Progress')
    rejected_requests = SourcingProductRequest.objects.filter(status='Rejected')
    return render(request, 'staff_panel/sourcing_requests.html',{'completed_requests':completed_requests,
                                                           'pending_requests':pending_requests,
                                                           'in_progress_requests':in_progress_requests,
                                                           'rejected_requests':rejected_requests})

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def update_sourcing_req_status(request):
    if request.method == 'POST':
        id = request.POST['request_id']
        status = request.POST['status']
        review = request.POST['review']
        user = request.user.username

        try:
            req = get_object_or_404(SourcingProductRequest, id=id)
            req.status = status
            req.review = review
            req.updated_by = user
            req.save()

            messages.success(request, 'Status updated successfully!')
            return redirect('staff_sourcing_requests')
        except Exception as e:
            logging.error(f'unable to update: {str(e)}')
            messages.error(request, 'Please try again later!')
            return redirect('staff_sourcing_requests')
        
@role_required('Staff')
@login_required(login_url='login')
@never_cache
def fetch_and_store_shopify_orders(request):
    stores = Shop.objects.all()
    
    for store in stores:
        try:
            shopify_url = f"https://{store.shop_name}.myshopify.com/admin/api/2023-01/orders.json?fields=id,total_price,created_at,financial_status,fulfillment_status,line_items"
            headers = {
                'Content-Type': 'application/json',
                'X-Shopify-Access-Token': store.access_token,
            }
            response = requests.get(shopify_url, headers=headers)
            
            if response.status_code == 200:
                orders_data = response.json().get('orders', [])
                for order_data in orders_data:
                    order, created = ShopifyOrder.objects.update_or_create(
                        order_id=order_data['id'],
                        defaults={
                            'total_price': order_data['total_price'],
                            'created_at': order_data['created_at'],
                            'payment_status': order_data.get('financial_status', ''),
                            'fulfillment_status': order_data.get('fulfillment_status', ''),
                            'shop':store,
                        }
                    )
                    # Update or create order items
                    for item_data in order_data.get('line_items', []):
                        product = MyProducts.objects.filter(product__name=item_data['name']).first()
                        ShopifyOrderItem.objects.update_or_create(
                            order=order,
                            product_name=item_data['name'],
                            defaults={
                                'product':product,
                                'quantity': item_data['quantity'],
                                'price': item_data['price'],
                            }
                        )
                messages.success(request, f'Successfully fetched orders from {store.shop_name}!')
            else:
                logging.error(f"Failed to fetch orders for store {store.shop_name}: {response.content}")
                messages.error(request, f"Failed to fetch orders for store {store.shop_name}!")

        except Exception as e:
            logging.error(f"Error fetching orders for store {store.shop_name}: {str(e)}")
            messages.error(request, f"An error occurred while fetching orders for store {store.shop_name}!")
    
    return redirect('staff_orders')

@role_required('Staff')
@login_required(login_url='login')
@never_cache
def orders(request):
    orders = ShopifyOrder.objects.prefetch_related('items').all()
    return render(request, 'staff_panel/orders.html',{'orders':orders})