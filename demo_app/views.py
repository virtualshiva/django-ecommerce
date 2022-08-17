
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . models import Product
from . forms import *
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from accounts.auth import admin_only
from userspage.models import Order

# Create your views here.

def index(request):
    return HttpResponse('This is form the demo app')

def test(request):
    return HttpResponse('This is a demo app second')

@login_required
@admin_only

def show_product(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'demo/index.html', context)

@login_required
@admin_only

def post_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'category added')
            return redirect('/admin/addcategory')
        else:
            messages.add_message(request,messages.ERROR, 'please verify forms fields')
            return render(request, 'demo/addcategory.html',{
                'form':form
            })


    context = {
        'form':CategoryForm
    } 
    return render(request, 'demo/addcategory.html', context)

@login_required
@admin_only

def post_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'product added')
            return redirect('/admin/addproduct')
        else:
            messages.add_message(request,messages.ERROR, 'please verify forms fields')
            return render(request, 'demo/addproduct.html',{
                'form':form
            })

    context = {
        'form': ProductForm
    }
    return render(request, 'demo/addproduct.html', context)

@login_required
@admin_only

def show_category(request):
    category = Category.objects.all()
    context={
        'category': category

    }
    return render(request, 'demo/category.html', context)

@login_required
@admin_only

def delete_category(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS,'category deleted')
    return redirect('/admin/category')

@login_required
@admin_only

def update_category_form(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'category updated')
            return redirect('/admin/category')
        else:
            messages.add_message(request, messages.ERROR, 'unable to update category')
            return render(request, 'demo/updatecategory.html', {
                'form': form
            })
    context = {
        'form': CategoryForm(instance=category)
    }
    return render(request, '/demo/updatecategory.html', context)

@login_required
@admin_only


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    os.remove(product.product_image.path)
    product.delete()

    messages.add_message(request, messages.SUCCESS, 'product deleted')
    return redirect('/admin/product')

@login_required
@admin_only

def product_update_form(request, product_id):   
    product = Product.objects.get(id = product_id)
    if request.method == 'POST':
        if request.FILES.get('product_image'):
            os.remove(product.product_image.path)
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product updated')
            return redirect('/admin/product')
        else:
            messages.add_message(request, messages.ERROR, 'failed ot update product')
            return render(request, 'demo/updateproduct.html', {'form':form})
    context={
        'form': ProductForm(instance=product)
        }
    return render(request, 'demo/updateproduct.html', context)

@login_required   
@admin_only
def user_order(request):
    items = Order.objects.all()
    context = {
        'items': items
    }
    return render(request, '/demo/usersorder.html', context)