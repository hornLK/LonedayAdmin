from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from utils.request_api import secret_apirequest
from utils.send_key import email_sendkey
from django.views.decorators.csrf import csrf_exempt
from authsweb.form import AddUserForm
import requests,json

# Create your views here.
#授权管理主页

@csrf_exempt
def auths_index(request):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    error=None
    msg = None
    try:
        if request.method == "POST":
            adduser_form = AddUserForm(request.POST)
            if adduser_form.is_valid():
                cd = adduser_form.cleaned_data
                int(cd.get("phonenumber"))
                cd["username"] = cd.get("email").strip().split("@")[0].replace(".","_")
                data = {"username":cd.get("username")}
                sync_url = settings.AUTHS_URL+"/apiv1/auths/user/syncjs"
                sync_result = json.loads(requests.post(sync_url,headers=headers,data=json.dumps(data)).text)
                if sync_result.get("status"):
                    adduser_url = settings.AUTHS_URL+"/apiv1/auths/user/create/"
                    create_result = json.loads(requests.post(adduser_url,headers=headers,data=json.dumps(cd)).text)
                    if not create_result.get("status"):
                        raise ValueError ("用户创建失败:"+str(create_result.get("error")))
                else:
                    raise ValueError("用户同步失败:"+str(sync_result.get("error")))
                print(create_result)
                if create_result.get("pubkey") and create_result.get("prikey"):
                    email_sendkey(cd.get('email'),create_result.get("pubkey"),create_result.get("prikey")) 
                else:
                    raise ValueError("用户创建成功，但密钥不可用")
                msg = "用户创建成功"
    except Exception  as e:
        print(e)
        error = str(e)
    adduser_form = AddUserForm()
    userlist_url = settings.AUTHS_URL+"/apiv1/auths/user/list/"
    hostlist_url = settings.AUTHS_URL+"/apiv1/auths/host/page/list/"
    rolelist_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
    aduitusers = json.loads(requests.get(userlist_url,headers=headers).text)
    aduithosts = json.loads(requests.get(hostlist_url,headers=headers).text)
    aduitroles = json.loads(requests.get(rolelist_url,headers=headers).text)
    data ={"aduitusersinfo":aduitusers,
            "aduithostscount":aduithosts.get("count",0),
            "aduitroles":aduitroles.get("roles"),
            "error":error,
	    "msg":msg
           }
    return render(request,"authManager/auths_index.html",
                          {"data":data,"addUserForm":adduser_form,"status":True}
                )

@csrf_exempt
def AuthsUserDetail(request):
    return render(request,"authManager/user_detail.html")

@csrf_exempt
def delUserHost(request):
    if request.method == "POST":
        ajax_data=request.POST.get("data")
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        deluserhost_url = settings.AUTHS_URL+"/apiv1/auths/user/delhost/"
        result = requests.post(deluserhost_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
#index界面中编辑用户信息的按钮
@csrf_exempt
def authorizeEditUser(request):
    if request.method == "POST":
        ajax_data=request.POST.get("data")
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        useredit_url = settings.AUTHS_URL+"/apiv1/auths/user/edit/"
        result = requests.post(useredit_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
    else:

        return HttpResponse(json.dumps({"status":False,"message":"method error"}),
                            content_type="application/json")
#获取登录角色
@csrf_exempt
def authorizeGetRoles(request):
    if request.method == "GET":
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        try:
            role_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
            role_dic = json.loads(requests.get(role_url,headers=headers).text)
            role_list = json.dumps(role_dic.get("roles"))
            return HttpResponse(role_list,content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"status":False,"message":e}),
                                            content_type="application/json")
#编辑保存角色
@csrf_exempt
def authorizeEditUserRole(request):
    if request.method == "POST":
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        ajax_data=request.POST.get("data")
        userroleedit_url = settings.AUTHS_URL+"/apiv1/auths/userrole/edit/"
        result = requests.post(userroleedit_url,headers=headers,data=ajax_data).text
        return HttpResponse(result,content_type="application/json")
#为用户添加主机访问权限
@csrf_exempt
def authorizeAddUserRole(request,user_id):
    try:
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        page = request.GET.get("page",1)
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        #outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/out-list/"
        outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/out-list/"
        role_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        out_hosts = json.loads(requests.get(outhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text)
        roles = json.loads(requests.get(role_url,headers=headers).text).get("roles")
        data = {
                    "hosts_info":out_hosts,
                    "user_info":user_res.get("user_info"),
                    "role_info":roles
                }
        return render(request,"authManager/authorizeAddUserRole.html",
                      {"data":data,"status":True})
    except Exception as e:
        print(e)
        return render(request,"authManager/authorizeAddUserRole.html")

#为用户添加授权主机
@csrf_exempt
def AuthsUserAddHosts(request,user_id):
    try:
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        page = request.GET.get("page",1)
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/out-list/"
        role_url = settings.AUTHS_URL+"/apiv1/auths/role/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        out_hosts = json.loads(requests.get(outhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text)
        roles = json.loads(requests.get(role_url,headers=headers).text).get("roles")
        data = {
                    "hosts_info":out_hosts,
                    "user_info":user_res.get("user_info"),
                    "role_info":roles
                }
        return render(request,"authManager/auths_add_hosts.html",
                      {"data":data,"status":True})
    except Exception as e:
        print(e)
        return render(request,"authManager/auths_add_hosts.html")

#管理用户登录权限
def authorizeUser(request,user_id):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        page = request.GET.get("page",1)
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        userhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        userhosts_res = json.loads(requests.get(userhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text)
        data = {
                "user_hosts":userhosts_res,
                "user_info":user_res.get("user_info")
            }
        return render(request,"authManager/authorizeUser.html",{
            "data":data,"status":True
        })
    except Exception as e:
        print(e)
        return render(request,"authManager/authorizeUser.html")

#管理用户登录主机与角色
def UserHosts(request,user_id):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        authuser_url = settings.AUTHS_URL+"/apiv1/auths/user/info/"
        userhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/list/"
        user_res = json.loads(requests.get(authuser_url,headers=headers,params={"user_id":user_id}).text)
        userhosts_res = json.loads(requests.get(userhosts_url,headers=headers,params={"user_id":user_id}).text)
        data = {
                "user_hosts":userhosts_res,
                "user_info":user_res.get("user_info")
            }
        return render(request,"authManager/auths_user_hosts.html",{
            "data":data,"status":True
        })
    except Exception as e:
        print(e)
        return render(request,"authManager/auths_user_hosts.html",{"status":False,"error":str(e)})

#ajax分页获取不属于用户的机器
def authorizeUserOutHosts(request,user_id):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        if request.method == "GET":
            page = request.GET.get("page",1)
            outhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/hosts/page/out-list/"
            out_hosts = requests.get(outhosts_url,headers=headers,params={"user_id":user_id,"page":int(page)}).text
            return HttpResponse(out_hosts,content_type="application/json")
    except Exception as e:
        print(e)
        return HttpResponse({"status":False},content_type="application/json")

#ajax添加用户主机授权
@csrf_exempt
def authorizeAuthHostsUser(request):
    headers = secret_apirequest(settings.AUTHS_SECRETKEY)
    try:
        if request.method == "POST":
            data = request.POST.get("data")
            authhosts_url = settings.AUTHS_URL+"/apiv1/auths/user/authshosts/"
            res = requests.post(authhosts_url,headers=headers,data=data).text
            print(res)
            return HttpResponse(res,content_type="application/json")
    except Exception as e:
            return HttpResponse({"status":res},content_type="application/json")
