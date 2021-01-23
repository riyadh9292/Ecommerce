from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib.auth import authenticate,login,get_user_model
from django.http import JsonResponse,HttpResponse


def home(request):
    #print(request.session.get("first_name","me"))
    print(request.session.get("user","jumbo"))
    context={
            "title":"hi",
            "content":"durosa",
            "premium":"loca"
        }
    return render(request,"home.html",context)

def about(request):

    context={
            "title":"about",
            "content":"its about",
        }

    if request.user.is_authenticated():
        context["premier"]="that is something else"
    return render(request,"about.html",context)






def contact(request):
    contact_form=ContactForm(request.POST or None)
    context={
        "title":"Contact",
        "form":contact_form,
        "brand":"new brand name"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"message":"Thank You for submitting data"})
    if contact_form.errors:
        print(contact_form.cleaned_data)
        errors=contact_form.errors.as_json()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(errors,status=400,content_type='application/json')
    return render(request,"contact.html",context)
