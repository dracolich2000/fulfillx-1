from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from staff_panel.models import Products, SourcingProductRequest
from django.contrib import messages
from fulfillX.access_control_decorater import role_required
import shopify
from django.conf import settings
from django.http import HttpResponse
import urllib.parse
import requests
from .models import Shop, ShopifyOrder, ShopifyOrderItem, MyProducts
from django.core.exceptions import ObjectDoesNotExist
import logging

# Create your views here.
@role_required('User')
@login_required(login_url='login')
@never_cache
def usr_dashboard(request):
    return render(request, 'user_panel/dashboard.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def custom_products(request):
    return render(request, 'user_panel/custom_products.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def find_products(request):
    products = Products.objects.all()
    return render(request, 'user_panel/find_products.html',{'products':products})

@role_required('User')
@login_required(login_url='login')
@never_cache
def import_list(request):
    return render(request, 'user_panel/import_list.html')

@role_required('User')
@login_required(login_url='login')
@never_cache
def manage_store(request):
    user = request.user.username
    shops = Shop.objects.filter(linked_by=user)
    return render(request, 'user_panel/manage_store.html',{'shops':shops})

@role_required('User')
@login_required(login_url='login')
@never_cache
def my_products(request):
    user = request.user.username
    shops = Shop.objects.filter(linked_by=user)
    store_id = request.GET.get('store')
    if store_id:
        products = MyProducts.objects.filter(shop_id=store_id)
    else:
        products = MyProducts.objects.filter(shop__in=shops)
    return render(request, 'user_panel/my_products.html',{'shops':shops,
                                                          'products':products})

@role_required('User')
@login_required(login_url='login')
@never_cache
def view_product(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    stores = Shop.objects.filter(linked_by=request.user.username)
    return render(request, 'user_panel/view_product.html',{'product':product,
                                                     'stores':stores})

@role_required('User')
@login_required(login_url='login')
@never_cache
def sourcing(request):
    username = request.user.username
    sourcing_requests = SourcingProductRequest.objects.filter(added_by=username)
    return render(request, 'user_panel/sourcing.html',{'sourcing_requests':sourcing_requests})

@role_required('User')
@login_required(login_url='login')
@never_cache
def new_sourcing_request(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        link = request.POST['product_link']
        image = request.FILES.get('product_image')
        description = request.POST['description']
        username = request.user.username

        try:
            SourcingProductRequest.objects.create(
                name=name,
                link=link,
                image=image,
                description=description,
                added_by = username
            )
            messages.success(request, 'Request submitted! Please check request status for updates.')
            return redirect('user_sourcing')
        except:
            messages.error(request, 'Please try again after some time!')
            return redirect('user_sourcing')

@role_required('User')
@login_required(login_url='login')
@never_cache
def shopify_callback(request):
    # Ensure the request is a GET request
    if request.method != 'GET':
        return HttpResponse("Invalid request method. Expected GET.", status=400)
    
    # Retrieve the 'shop' and 'code' parameters from the GET request
    shop = request.GET.get('shop')
    code = request.GET.get('code')

    # Validate that 'shop' and 'code' are present
    if not shop or not code:
        return HttpResponse("Missing 'shop' or 'code' parameters.", status=400)

    # Exchange the code for an access token
    url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": settings.SHOPIFY_API_KEY,
        "client_secret": settings.SHOPIFY_API_SECRET,
        "code": code,
    }

    # Send POST request to exchange the code for an access token
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        shop_info_url = f"https://{shop}/admin/api/2023-01/shop.json"
        headers = {"X-Shopify-Access-Token": access_token}
        shop_response = requests.get(shop_info_url, headers=headers)

        if shop_response.status_code == 200:
                shop_data = shop_response.json().get('shop', {})
                shop_name = shop_data.get('name', 'Unknown Shop')

        Shop.objects.create(
            shop_name=shop_name,
            shop_url=shop,
            access_token=access_token,
            shop_platform="Shopify",
            linked_by=request.user.username
        )
        return redirect('usr_dashboard')  # Redirect to your dashboard or desired page
    else:
        return HttpResponse(f"Failed to get access token: {response.text}", status=400)
    
@role_required('User')
@login_required(login_url='login')
@never_cache
def shopify_auth(request):
    shopify_api_key = settings.SHOPIFY_API_KEY
    redirect_uri = settings.SHOPIFY_REDIRECT_URI
    scopes = "read_products,write_products,read_orders,write_orders,read_fulfillments,write_fulfillments,read_inventory,write_inventory,read_shopify_payments_payouts"
    if request.method == 'POST':
        shop = request.POST['shop']
        if not shop:
            return HttpResponse("Missing 'shop' parameter.", status=400)

    # Construct the OAuth URL
    oauth_url = f"https://{shop}/admin/oauth/authorize"
    params = {
        "client_id": shopify_api_key,
        "scope": scopes,
        "redirect_uri": redirect_uri,
    }
    full_url = f"{oauth_url}?{urllib.parse.urlencode(params)}"

    return redirect(full_url)



@role_required('User')
@login_required(login_url='login')
@never_cache
def push_to_shopify(request):
    if request.method == "POST":
        product_id = request.POST['product_id']
        store_name = request.POST['store']
        product_price = request.POST['price']
        
        try:
            # Fetch the product based on product_id
            product = Products.objects.get(id=product_id)
        except ObjectDoesNotExist:
            messages.error(request, "Product not found!")
            return redirect('find_products')
        
        try:
            # Select the store using store_name
            store = Shop.objects.get(shop_name=store_name)
        except ObjectDoesNotExist:
            messages.error(request, "Shop not found!")
            return redirect('find_products')
        
        # Prepare the product data for Shopify API
        shopify_url = f"https://{store.shop_name}.myshopify.com/admin/api/2023-01/products.json"
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': store.access_token,  # Ensure token has the correct permissions
        }
        
        # Create the product data
        product_data = {
            "product": {
                "title": product.name,
                "body_html": product.description,
                "vendor": product.vendor,
                "product_type": product.category,
                "variants": [
                    {
                        "price": product_price,
                    }
                ],
                "images": [
                    {
                        "src": image.image_url  # Ensure the image URL is valid
                    } for image in product.images.all()
                ]
            }
        }

        # Make the request to Shopify
        response = requests.post(shopify_url, json=product_data, headers=headers)

        # Handle response
        if response.status_code == 201:
            response_data = response.json()
            shopify_product_id = response_data['product']['id']
            
            MyProducts.objects.create(
                product=product,
                fulfillx_price=product.price,  # Assuming FulFillX price is the same as selling price
                selling_price=product_price,
                inventory=0,  # Default inventory as 0
                shopify_product_id=shopify_product_id,
                pushed_to_shopify=True,
                shop=store
            )
            
            messages.success(request, "Product pushed to Shopify successfully!")
        else:
            error_msg = response.json()  # Get detailed error message from Shopify API
            messages.error(request, f"Failed to push product to Shopify! Error: {error_msg}")
    
    return redirect('find_products')

@role_required('User')
@login_required(login_url='login')
@never_cache
def delete_store(request, store_id):
    store = get_object_or_404(Shop, id=store_id)
    try:
        store.delete()
        messages.success(request, 'Store deleted successfully!')
        return redirect('manage_store')
    except:
        messages.error(request,'Something went wrong. please try again!')
        return redirect('manage_store')

@role_required('User')
@login_required(login_url='login')
@never_cache
def fetch_and_store_shopify_orders(request):
    stores = Shop.objects.filter(linked_by=request.user.username)
    
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
                        }
                    )
                    # Update or create order items
                    for item_data in order_data.get('line_items', []):
                        ShopifyOrderItem.objects.update_or_create(
                            order=order,
                            product_name=item_data['name'],
                            defaults={
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
    
    return redirect('user_orders')

    
@role_required('User')
@login_required(login_url='login')
@never_cache
def orders(request):
    orders = ShopifyOrder.objects.prefetch_related('items').all()
    return render(request, 'user_panel/orders.html',{'orders':orders})