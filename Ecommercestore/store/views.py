from django.shortcuts import render
from . models import Category, Product
from django.shortcuts import get_object_or_404
from .forms import SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def store(request):
    all_products = Product.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(all_products, 10)

    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        all_products = paginator.page(1)
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)

    form = SearchForm()

    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            all_products = (Product.objects.filter(title__icontains=search) |
                        Product.objects.filter(brand__icontains=search))

    context = {'all_products': all_products, 'form': form}
    return render(request, 'store/store.html', context=context)
def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}


def list_category(request, slug=None):

    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category': category, 'products': products})
def product_info(request, slug):

    product = get_object_or_404(Product, slug=slug)

    context = {'product': product}

    return render(request, 'store/product-info.html', context=context)

