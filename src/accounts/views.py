from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate,login,get_user_model
from django.utils.http import is_safe_url
from .models import GuestModel
from django.views.generic import CreateView,FormView
from .signals import user_logged_in
# Create your views here.

def guest_register_user(request):

    form=GuestForm(request.POST or None)
    next=request.GET.get('next')
    next_post=request.POST.get('next')
    print(next)
    print(next_post)
    redirect_path = next_post or next or None
    if form.is_valid():
        email=form.cleaned_data.get("email")
        new_guest_email=GuestModel.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path[:-1])
        else:
            return redirect("/register/")

    return redirect("/register/")


class LoginView(FormView):
    form_class=LoginForm
    success_url='/'
    template_name='accounts/login.html'

    def form_valid(self,form):
        request=self.request
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path = next_post or next_ or None
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            user_logged_in.send(user.__class__,instance=user,request=request)
            print(user)
            try:
                del request.session['guest_email_id']
            except :
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path[:-1])
            else:
                return redirect("/")
        return super(LoginView,self).form_invalid(form)


#def login_user(request):

#    form=LoginForm(request.POST or None)
#    next_=request.GET.get('next')
#    next_post=request.POST.get('next')
#    redirect_path = next_post or next_ or None
#    if form.is_valid():
#        print(form.cleaned_data)
#        username=form.cleaned_data.get("username")
#        password=form.cleaned_data.get("password")
#        user=authenticate(request,username=username,password=password)
#        if user is not None:
#            login(request,user)
#            print(user)
#            try:
#                del request.session['guest_email_id']
#            except :
#                pass
#            if is_safe_url(redirect_path, request.get_host()):
#                return redirect(redirect_path[:-1])
#            else:
#                return redirect("/")
#        else:
#            print("error")

#    return render(request,"accounts/login.html",{"form":form})



class RegisterView(CreateView):
    form_class=RegisterForm
    template_name='accounts/register.html'
    success_url='/login/'

#User=get_user_model()

#def register_page(request):

#    form=RegisterForm(request.POST or None)
#    context={
#        "form":form
#    }
#    if form.is_valid():
#        print(form.cleaned_data)
#        form.save()
        #print(new_user)

#    return render(request,"accounts/register.html",context)
