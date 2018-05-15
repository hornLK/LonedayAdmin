from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import PermissionListForm
from .models import UserInfo,Role,Permission


def permission_verify():
    def decorator(view_func):
        def _wrapped_view(request,*args,**kwargs):
            User = UserInfo.objects.get(email = request.email)

            if not User.is_superuser:
                if not User.role:
                    return HttpResponseRedirect(reverse('permission_deny'))
                role_permission = Role.objects.get(name=User.role)
                role_permission_list = role_permission.permission.all()

                matchUrl = []
                for x in role_permission_list:
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)
                    else:
                        pass
                print("{----->matchUrl:{}}".format(request.user,str(matchUrl)))
                if len(matchUrl) == 0:
                    return HttpResponseRedirect(reverse("permission_deny"))
            else:
                pass
            return view_func(request,*args,**kwargs)
        return _wrapped_view

@login_required
def permission_deny(request):
    temp_name = 'main-header.html'
    kwargs = {
        'temp_name': temp_name,
        'request': request,
    }
    return render(request,'accounts/permission_deny.html',kwargs)

#@login_required
#@permission_verify()
def permission_add(request):
    temp_name = 'accounts/accounts-header.html'
    if request.method == "POST":
        form = PermissionListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
    else:
        form = PermissionListForm()

    kwargs = {
        "temp_name":temp_name,
        "form":form,
        "request":request,
    }
    return render(request,"accounts/permission_add.html",kwargs)

@login_required
#@permission_verify()
def permission_list(request):
   all_permission = Permission.objects.all()
   temp_name = "accounts/accounts-header.html"
   return render(request,'accounts/permission_list.html',locals())

@login_required
def permission_edit(request,ids):
    pass

@login_required
def permission_del(request,ids):
    pass
