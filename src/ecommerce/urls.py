"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from .views import home,contact,about
from accounts.views import LoginView,RegisterView,guest_register_user
from products.views import ProductListLiew,product_list_view,ProductDetailView,product_detail_view,ProductFeaturedListLiew,ProductFeaturedDetailView,ProductDetailSlugView
from carts.views import cart_home
from address.views import checkout_address_create_view,checkout_address_reuse_view
from carts.views import cart_detail_api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('contact/',contact,name="contact"),
    path('about/',about,name="about"),
    path('login/',LoginView.as_view(),name="login"),
    path('checkout/address/create/',checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse/',checkout_address_reuse_view,name="checkout_address_reuse"),
    path('register/guest/',guest_register_user,name="guest_register"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('api/cart/',cart_detail_api_view,name="api-cart"),
    #path('cart/',cart_home,name="cart"),
    path('cart/',include(("carts.urls",'carts'),namespace='carts')),
    path('register/',RegisterView.as_view(),name="register"),
    path('boot/',TemplateView.as_view(template_name="boot/boot.html"),name="boot"),
    path('products-fbv/',product_list_view,name="product_fb"),
    path('products/',include(("products.urls",'product'),namespace='product')),
    path('products-fbv/<int:pk>/',product_detail_view,name="product_details_fb"),
    #path('products/<int:pk>/',ProductDetailView.as_view(),name="products_details"),
    path('featured/',ProductFeaturedListLiew.as_view(),name="featured"),
    path('featured/<int:pk>/',ProductFeaturedDetailView.as_view(),name="featured-details"),
    #path('products/<slug:slug>/',ProductDetailSlugView.as_view(),name="products_details"),
    path('search/',include(("search.urls",'search'),namespace='search')),


]

if settings.DEBUG:
    urlpatterns=urlpatterns +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
