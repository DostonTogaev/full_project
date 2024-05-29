from itertools import product
from typing import Optional

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from apps.forms import ProductModelForm, CommentModelForm, OrderModelForm
from apps.models import Product, Category


# Create your views here.


def index_page(request, cat_id=None):
    filter_type = request.GET.get('filter', '')
    search_query = request.GET.get('search', '')
    categories = Category.objects.all()
    if cat_id:
        products = Product.objects.filter(category=cat_id)
        if filter_type == 'expensive':
            products = products.order_by('-price')
        elif search_query == 'cheap':
            products = products.ordey_by('price')
    else:
        products = Product.objects.all()
        if filter_type == 'expensive':
            products = products.order_by('-price')
        elif search_query == 'cheap':
            products = products.ordey_by('price')

    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) | Q(category__title__icontains=search_query))
    context = {
        'products': products,
        'categories': categories,

    }
    return render(request, 'apps/home.html', context)

    context = {
        'products': products,
        'categories': categories,

            }
    return render(request, 'apps/home.html', context)


def detail_product(request, product_id):
    product = Product.objects.get(id=product_id)
    price_lower_bound = product.price*0.8
    price_upper_bound = product.price*1.2

    comments = product.comments.filter(is_active=True).order_by('-created_at')
    # comments = product.comments.all().order_by('-created_at')
    # comments = product.comments.all().order_by('-created_at')[:3]
    similar_products = Product.objects.filter(Q(price__lte=price_upper_bound) & Q(price__gte = price_lower_bound)).exclude(id=product_id)
    count = product.comments.count()
    context = {
        'product': product,
        'comments': comments,
        'count': count,
        'similar_products':similar_products
    }

    return render(request, 'apps/detail.html', context)


# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = request.POST['name']
#             description = request.POST['description']
#             price = request.POST['price']
#             image = request.FILES['image']
#             rating = request.POST['rating']
#             discount = request.POST['discount']
#             product = Product(name=name, description=description, price=price, image=image, rating=rating,
#                               discount=discount)
#             product.save()
#             return redirect('index')
#
#     else:
#         form = ProductForm()
#     return render(request, 'app/add-product.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ProductModelForm()

    context = {
        'form': form,
    }
    return render(request, 'apps/add-product.html', context)


def add_comment(request, product_id):
    # product = Product.objects.get(id=product_id)
    product = get_object_or_404(Product, id=product_id)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', product_id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'apps/detail.html', context)

def expensive_product(request):
    products = Product.objects.filter(price__gt=100000)
    context = {
        'products': products,
    }
    return render(request, 'apps/home.html', context)

def cheap_product(request):
    products = Product.objects.filter(price__lt=100000)
    context = {
        'products': products,
    }
    return render(request, 'apps/home.html', context)

def add_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(order=False)
            order.product = product
            order.save()
            return redirect('detail', product_id)

    context = {
        'form': form,
        'product':product
    }

    return render(request, 'apps/detail.html', context)