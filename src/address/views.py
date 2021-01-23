from django.shortcuts import render,redirect
from .form import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from .models import Address
# Create your views here.


def checkout_address_create_view(request):
    form=AddressForm(request.POST or None)
    context={"form":form}
    next=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path = next_post or next or None
    if form.is_valid():
        print(request.POST)
        instance=form.save(commit=False)
        billing_profile,guest_billing_profile_created=BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type=request.POST.get('address_type','shipping')
            instance.billing_profile=billing_profile
            instance.address_type=address_type
            instance.save()

            request.session[address_type+"_address_id"]=instance.id
            print(address_type+"_address_id")
        else:
            print("error here")
            return redirect("/cart:checkout/")
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path[:-1])
    return redirect("/cart:checkout/")



def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context={}
        next=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path = next_post or next or None
        if request.method == "POST":
            print(request.POST)
            shipping_address=request.POST.get('shipping_address',None)
            address_type=request.POST.get('address_type','shipping')
            billing_profile,guest_billing_profile_created=BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs=Address.objects.filter(billing_profile=billing_profile,id=shipping_address)
                if qs.exists():
                    request.session[address_type+"_address_id"]=shipping_address

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path[:-1])
    return redirect("/cart:checkout/")
