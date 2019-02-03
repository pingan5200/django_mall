from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Slide

from cart.forms import CartAddProductForm
from .recommender import Recommender


# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(isHome=True, available=True)

    # 轮播图
    slides = Slide.objects.all()

    # 商品排名
    r = Recommender()
    rank_products = r.get_best_saled()

    context = {
        'categories': categories,
        'products': products,
        'slides': slides,
        'rank_products': rank_products
    }
    return render(request, 'shop/base.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    # 商品推荐
    r = Recommender()
    re_products = r.suggest_products_for([product], 5)

    context = {
        'cart_product_form': cart_product_form,
        'product': product,
        're_products': re_products
    }
    return render(request,
                  'shop/product/detail.html',
                  context)