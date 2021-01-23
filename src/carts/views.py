from django.shortcuts import render,redirect
from .models import Cart
from django.http import JsonResponse
from products.models import  Product
from orders.models import Order
from address.models import Address
from accounts.forms import LoginForm,GuestForm
from billing.models import BillingProfile
from accounts.models import GuestModel
from address.form import AddressForm
# Create your views here.

#def create_cart(user=None):
#    cart_obj=Cart.objects.create(user=None)
#    print("creating new cart ")
#    return cart_obj
def cart_detail_api_view(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    products=[{
        "id":x.id,
        "url":x.get_absolute_url(),
        "name":x.name,
        "price":x.price

        } for x in cart_obj.products.all()]
    cart_data={"products":products,"subtotal":cart_obj.subtotal,"total":cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    #products=cart_obj.products.all()
    #total=0
    #for x in products:
    #    total+=x.price
    #print(total)
    #cart_obj.total = total
    #cart_obj.save()
    #del request.session['cart_id']
    #request.session['cart_id']="123"
    #cart_id=request.session.get("cart_id",None)

    #if cart_id is None:
    #    cart_obj=create_cart()
    #    request.session['cart_id']=cart_obj.id
    #    print("new cart")
    #else:
    #qs=Cart.objects.filter(id=cart_id)
    #if qs.count()==1:
    #    print("Cart ID exists")
    #    cart_obj=qs.first()
    #    if request.user.is_authenticated and cart_obj.user is None:
    #        cart_obj.user=request.user
    #        cart_obj.save()
    #else:
    #    cart_obj= Cart.objects.new(user=request.user)
    #    request.session['cart_id']=cart_obj.id
        #cart_obj=Cart.objects.get(id=cart_id)
#    print(request.session.se)
#    print(dir(request.session))
    #print(request.session.session_key)
    #request.session['cart_id']=12
    #request.session['user']=request.user.username
    return render(request,"carts/home.html",{"cart":cart_obj})



def cart_update(request):
    #print(request.POST)
    product_id=request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Produuct does not exists")
            return redirect("cart:home")
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added=False
        else:
            cart_obj.products.add(product_obj)
            added=True
        request.session['cart_items']=cart_obj.products.count()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("Ajax request")
            json_data={
                "added": added,
                "removed": not added,
                "cartItemsCount": cart_obj.products.count()

            }
            return JsonResponse(json_data,status=200)

    #return redirect(product_obj.get_absolute_url())
    return redirect("carts:home")



def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("carts:home")
    #user=request.user
    #billing_profile=None
    loging_form=LoginForm()
    guest_form=GuestForm()
    address_form=AddressForm()
    #billing_address_form=AddressForm()
    billing_address_id=request.session.get("billing_address_id",None)
    shipping_address_id=request.session.get("shipping_address_id",None)
    billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
    address_qs=None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs=Address.objects.filter(billing_profile=billing_profile)

        order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id:
            order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address=Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

        if request.method=="POST":
            #del request.session['cart_id']
            is_done=order_obj.check_done()
            if is_done:
                order_obj.mark_paid()
                del request.session['cart_id']
                del request.session['cart_items']
                return redirect("carts:success")
        #order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        #if order_qs.count()==1:
        #    order_obj=order_qs.first()
        #else:
            #old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            #if old_order_qs.exists():
            #    old_order_qs.update(active=False)
        #    order_obj=Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
        #order_qs=Order.objects.filter(cart=cart_obj,active=True)
        #if order_obj.exists():
        #    order_qs.update(active=False)
        #else:
        #    order_obj,new_obj=Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
    context={
        "object":order_obj,
        "billing_profile":billing_profile,
        "login_form":loging_form,
        "guest_form":guest_form,
        "address_form":address_form,
        "address_qs":address_qs
        #"billing_address_form":billing_address_form
    }
    return render(request,"carts/checkout.html",context)


def checkout_done_view(request):
    return render(request,"carts/checkout-done.html",context={})
