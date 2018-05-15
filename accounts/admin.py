from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import UserInfo,Permission,Role

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ('email','nickname')

    def clean_Password2(self):
        password1 = self.cleaned_data.get("password1",None)
        password2 = self.cleaned_data.get("password2",None)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserInfo
        fields = ('email','nickname','role','is_active','is_superuser')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','nickname','role','is_active','is_superuser')
    list_filter = ('is_superuser','is_active','role')
    fieldsets = (
        ('基础',{'fields':('email','nickname')}),
        ('权限',{'fields':('role','is_superuser')}),
        ('状态',{'fields':('is_active',)})
    )
    add_fieldsets = (
        (None,{
                'classes':('wide',),
                'fields':('email','nickname','password1','password2','role','is_active','is_superuser')
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
# Register your models here.
admin.site.register(UserInfo,UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.unregister(Group)
