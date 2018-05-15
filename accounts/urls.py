"""LonedayAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path,include
from accounts import user,role,permission
urlpatterns = [
    re_path(r'^login/',user.login,name='login'),
    re_path(r'^logout/',user.logout,name='logout'),
    re_path(r'^user/list/$',user.user_list,name='user_list'),
    re_path(r'^user/add/$',user.user_add,name='user_add'),
    re_path(r'^user/delete/(?P<ids>\d+)/$',user.user_del,name='user_delete'),
    re_path(r'^user/edit/(?P<ids>\d+)/$',user.user_edit,name='user_edit'),
    re_path(r'^user/detail/(?P<ids>\d+)/$',user.user_detail,name='user_detail'),
    re_path(r'^reset/password(?P<ids>\d+)/$',user.reset_password,name='reset_password'),
    re_path(r'^change/password/$',user.change_password,name="change_password"),
    re_path(r'^role/add/$',role.role_add,name='role_add'),
    re_path(r'^role/list/$',role.role_list,name='role_list'),
    re_path(r'^role/edit/role-edit-(?P<ids>\d+)/$',role.role_edit,name='role_edit'),
    re_path(r'^role/detail/role-detail-(?P<ids>\d+)/$',role.role_detail,name='role_detail'),
    re_path(r'^role/detail/role-permission-detail-(?P<ids>\d+)/$',role.role_permission_detail,name='role_permission_detail'),
    re_path(r'^role/delete/role-delete-(?P<ids>\d+)/$',role.role_del,name='role_delete'),
    re_path(r'^permission/deny/$',permission.permission_deny,name='permission_deny'),
    re_path(r'^permission/add/$',permission.permission_add,name='permission_add'),
    re_path(r'^permission/list/$',permission.permission_list,name='permission_list'),
    re_path(r'^permission/edit/permission-edit-(?P<ids>\d+)/$',permission.permission_edit,name='permission_edit'),
    re_path(r'^permission/delete/permission-delete-(?P<ids>\d+)/$',permission.permission_del,name='permission_delete'),
]
