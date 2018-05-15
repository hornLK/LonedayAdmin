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
from django.contrib import admin
from django.urls import path,re_path,include
from . import  views , asset
urlpatterns = [
    #re_path(r'^$',asset.index,name="cmdb_index"),
    #re_path(r'^asset/add/$',asset.asset_add,name="asset_add"),
    #re_path(r'^business/list/$',business.buiness_list,name="business_list"),
    #re_path(r'^business/detail/(?P<ids>\d+)/$',business.buiness_detail,name="business_detail"),
]
