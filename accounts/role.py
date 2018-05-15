from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RoleListForm
from .models import Role
from accounts.permission import permission_verify


#@login_required
def role_add(request):
    temp_name = "accounts/accounts-header.html"
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm()
    kwargs = {
        "temp_name":temp_name,
        "form":form,
        "request":request,
    }
    return render(request,'accounts/role_add.html',kwargs)

@login_required
def role_list(request):
    temp_name = "accounts/accounts-header.html"
    all_role = Role.objects.all()
    return render(request,"accounts/role_list.html",locals())

@login_required
def role_edit(request,ids):
    role = Role.objects.get(id=ids)
    temp_name = "accounts/accounts-header.html"
    if request.method == "POST":
        form =RoleListForm(request.POST,instance=role)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        form = RoleListForm(instance=role)

    kwargs = {
        "temp_name":temp_name,
        "ids":ids,
        "form":form,
        "request":request,
    }
    return render(request,"accounts/role_edit.html",kwargs)

@login_required
def role_del(request,ids):
    Role.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse("role_list"))

@login_required
def role_detail(request,ids):
    temp_name = "accounts/accounts-header.html"
    role = Role.objects.get(id=ids)
    kwargs = {
        "temp_name":temp_name,
        "ids":ids,
        "role":role,
    }
    return render(request,"accounts/role_detail.html",kwargs)


@login_required
def role_permission_detail(request,ids):
    temp_name = "accounts/accounts-header.html"
    role = Role.objects.get(id=ids)
    print(role.name,role.permission)
    kwargs = {
        "tmep_name":temp_name,
        "ids":ids,
        "role":role,
    }
    return render(request,"accounts/role_permission_detail.html",kwargs)
