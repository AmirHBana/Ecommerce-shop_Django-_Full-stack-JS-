from django.urls import path
from . import views

urlpatterns = [

    # Store main page
    path('', views.store, name='store'),


    # Individual_product

    path('product/<slug:slug>', views.product_info, name='product-info'),

    # Individual_product

    path('search/<slug:slug>', views.list_category, name='list-category'),


]
