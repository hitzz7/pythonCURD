from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import json

from .models import (
    Product, Category, Cart, CartItem, Customer, Order, OrderItem, Payment
)

def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'app/home.html', context)

def product_list(request):
    """Product listing with filtering and pagination"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Category filtering
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Price sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'sort_by': sort_by,
    }
    return render(request, 'app/product_list.html', context)

def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'app/product_detail.html', context)

def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            cart, created = Cart.objects.get_or_create(customer=customer)
        except Customer.DoesNotExist:
            # Create customer if doesn't exist
            customer = Customer.objects.create(
                user=request.user,
                name=request.user.get_full_name() or request.user.username,
                email=request.user.email,
                phone='',
                address=''
            )
            cart, created = Cart.objects.get_or_create(customer=customer)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart

@csrf_exempt
def add_to_cart(request):
    """Add product to cart via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            if quantity > product.stock_quantity:
                return JsonResponse({
                    'success': False, 
                    'message': 'Not enough stock available'
                })
            
            cart = get_or_create_cart(request)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock_quantity:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Not enough stock available'
                    })
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart',
                'cart_total': cart.total_items
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def cart_view(request):
    """Shopping cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'app/cart.html', context)

@csrf_exempt
def update_cart_item(request):
    """Update cart item quantity"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity'))
            
            cart = get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            if quantity <= 0:
                cart_item.delete()
                message = 'Item removed from cart'
            else:
                if quantity > cart_item.product.stock_quantity:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Not enough stock available'
                    })
                cart_item.quantity = quantity
                cart_item.save()
                message = 'Cart updated'
            
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_total': cart.total_items,
                'cart_amount': float(cart.total_amount)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')
    
    if request.method == 'POST':
        # Process checkout form
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes', '')
        
        # Create or get customer
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': customer_name,
                    'email': customer_email,
                    'phone': customer_phone,
                    'address': shipping_address
                }
            )
        else:
            customer, created = Customer.objects.get_or_create(
                email=customer_email,
                defaults={
                    'name': customer_name,
                    'phone': customer_phone,
                    'address': shipping_address
                }
            )
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=cart.total_amount,
            shipping_address=shipping_address,
            phone_number=customer_phone,
            email=customer_email,
            notes=notes
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update stock
            cart_item.product.stock_quantity -= cart_item.quantity
            cart_item.product.save()
        
        # Create payment
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=cart.total_amount
        )
        
        # Clear cart
        cart.items.all().delete()
        
        if payment_method == 'cod':
            # Cash on Delivery
            payment.payment_status = 'pending'
            payment.save()
            order.status = 'confirmed'
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.order_id)
        
        elif payment_method == 'esewa':
            # Redirect to eSewa
            return redirect('esewa_payment', order_id=order.order_id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'app/checkout.html', context)

def esewa_payment(request, order_id):
    """Initiate eSewa payment"""
    order = get_object_or_404(Order, order_id=order_id)
    
    # eSewa parameters
    esewa_data = {
        'tAmt': str(order.total_amount),
        'amt': str(order.total_amount),
        'txAmt': '0',
        'psc': '0',
        'pdc': '0',
        'scd': settings.ESEWA_MERCHANT_ID,
        'pid': str(order.order_id),
        'su': settings.ESEWA_SUCCESS_URL,
        'fu': settings.ESEWA_FAILURE_URL
    }
    
    context = {
        'order': order,
        'esewa_data': esewa_data,
    }
    return render(request, 'app/esewa_payment.html', context)

def esewa_success(request):
    """eSewa payment success callback"""
    if request.method == 'GET':
        oid = request.GET.get('oid')
        amt = request.GET.get('amt')
        refId = request.GET.get('refId')
        
        try:
            order = Order.objects.get(order_id=oid)
            payment = order.payment
            
            # Verify payment with eSewa (in production)
            # For demo purposes, we'll mark as completed
            payment.payment_status = 'completed'
            payment.esewa_ref_id = refId
            payment.save()
            
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.save()
            
            messages.success(request, 'Payment successful!')
            return redirect('order_success', order_id=order.order_id)
            
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('home')

def esewa_failure(request):
    """eSewa payment failure callback"""
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('cart')

def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, order_id=order_id)
    context = {'order': order}
    return render(request, 'app/order_success.html', context)

def order_history(request):
    """User order history"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view order history.')
        return redirect('home')
    
    try:
        customer = Customer.objects.get(user=request.user)
        orders = customer.orders.all()
    except Customer.DoesNotExist:
        orders = []
    
    context = {'orders': orders}
    return render(request, 'app/order_history.html', context)