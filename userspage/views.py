from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import messages
from demo_app.models import *
from django.contrib.auth.decorators import login_required
from accounts.auth import user_only
from .models import Cart, Order
from .forms import OrderForm
from .filters import ProductFilter


# Create your views here.
 

def homepage(request):
    products = Product.objects.all().order_by('-id')[:8]
    context = {
        'products': products
    }

    return render(request, 'client/homepage.html', context)


def products(request):
    products = Product.objects.all().order_by('-id')
    product_filter = ProductFilter(request.GET, queryset=products)
    product_final = product_filter.qs
    context = {
        'products': product_final,
        'product_filter':product_filter
    }
    return render(request, 'client/products.html', context)


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'client/productdetails.html', context)


@login_required
@user_only
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_item_presence = Cart.objects.filter(user=user, product=product)
    if check_item_presence:
        messages.add_message(request, messages.ERROR,
                             'Product already present in the cart')
        return redirect('/mycart')
    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS,
                                 'Items added to cart')
            return redirect('/mycart')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Unable to add to cart')
            return redirect('/products')


@login_required
@user_only
def show_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request, 'client/cart.html', context)


@login_required
@user_only
def order_form(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = product.product_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            payment_method = request.POST.get('payment_method')
            payment_status = request.POST.get('payment_status')
            status = request.POST.get('status')

            order = Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status,
                status=status,
            )
            if order.payment_method == 'Cash On Delivery':
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                messages.add_message(
                    request, messages.SUCCESS, 'Order Successful')
                return redirect('/myorder')
            elif order.payment_method == 'Esewa':
                context = {
                    'order': order,
                    'cart': cart_item
                }
                return render(request, 'client/esewa_payment.html', context)
            else:
                messages.add_message(
                    request, messages.ERROR, 'Something went worng')
                return render(request, 'client/orderform.html', {'form': form})

    context = {
        'form': OrderForm
    }
    return render(request, 'client/orderform.html', context)


@login_required
@user_only
def show_order_items(request):
    user = request.user
    items = Order.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request, 'client/order.html', context)

import requests as req
def esewa_verify(request):
    import xml.etree.ElementTree as ET
    o_id = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')

    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amount,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': o_id,
    }
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        order_id = o_id.split("_")[0]
        order = Order.objects.get(id = order_id)
        order.payment_status = True
        order.save()
        cart_id = o_id.split("_")[1]
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        messages.add_message(request, messages.SUCCESS, 'payment successful')
        return redirect('/myorder')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to make payment')
        return redirect('/mycart')

@login_required
@user_only
def remove_cart_items(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request,messages.SUCCESS, 'items removed from the cart')
    return redirect('/mycart')




