from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .forms import LoginUserForm, AddUserForm
from .models import UserInfo
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def login(request):
    error_msg = ""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == 'GET' and request.GET.get('next',None):
        next_page = request.GET.get('next',None)
    else:
        next_page = reverse("index")
    if next_page == reverse('logout'):
        next_page = reverse('login')
    if request.method == 'POST':
        form = LoginUserForm(request,data=request.POST)
        if form.is_valid():
            auth.login(request,form.get_user())
            return HttpResponseRedirect(request.POST.get("next",reverse("index")))
        else:
            print(form.errors)
            error_msg = form.errors

    else:
        form = LoginUserForm(request)
    kwargs = {
        'request':request,
        'form':form,
        'next':next_page,
        'error_msg':error_msg,
    }
    return render(request,'accounts/login.html',kwargs)
@login_required
def logout(request):
    auth.logout(request)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponseRedirect(reverse("login"))


@login_required
def user_list(request):
    temp_name = "accounts/accounts-header.html"
    all_user = UserInfo.objects.all()
    kwargs = {
        "temp_name":temp_name,
        "all_user":all_user,
    }
    return render(request,"accounts/user_list.html",kwargs)

@login_required
def user_add(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect(reverse("user_list"))
    else:
        form = AddUserForm()
    kwargs = {
        "form":form,
        "request":request,
        "temp_name":temp_name,
    }
    return render(request,"accounts/user_add.html",kwargs)

@login_required
def user_del(required,ids):
    pass

@login_required
def user_edit(request,ids):
    pass
@login_required
def user_detail(request,ids):
    pass
@login_required
def reset_password(request,ids):
    pass

@login_required
def change_password(request):
    pass
