from django import forms
from django.contrib import auth
from .models import UserInfo, Role, Permission


class LoginUserForm(forms.Form):
    email = forms.EmailField(label="邮箱",
                             required=True,
                             error_messages={'required':"邮箱不能为空"},
                             widget=forms.EmailInput(attrs={'class':'form-control',
                                                            "placeholder":"邮箱"}))
    password = forms.CharField(label="密码",
                               required=True,
                               error_messages={'required':'密码不能为空'},
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 "placeholder":"密码"})
                              )
    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        self.user_cache = None
        super(LoginUserForm,self).__init__(*args,**kwargs)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = UserInfo.objects.get(email=email)
        except UserInfo.DoesNotExist:
            raise forms.ValidationError("用户不存在，请联系管理员")
        if user.check_password(password):
            self.user_cache = user
        else:
            raise forms.ValidationError('邮箱密码不匹配')
        if not self.user_cache.is_active:
            raise forms.ValidationError('账号已被禁用，请联系管理员')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class AddUserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('password','email','nickname','role','is_active')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.TextInput(attrs={'class':'form-control',"type":"password"}),
            'nickname':forms.TextInput(attrs={'class':'form-control'}),
            'role':forms.Select(attrs={'class':'form-control'}),
            'is_active':forms.Select(choices=((True,'启用'),(False,'禁用')),attrs={'class':'form-control'})
        }
    def __init__(self,*args,**kwargs):
        super(AddUserForm,self).__init__(*args,**kwargs)
        self.fields['email'].label = '邮箱'
        self.fields['email'].error_messages = {'required':'请输入邮箱',
                                               'invalid':'无效的邮箱格式'}
        self.fields['password'].label = '密码'
        self.fields['password'].error_messages = {'required':'请输入密码'}
        self.fields['nickname'].label = '姓名'
        self.fields['nickname'].error_messages = {'required':'请输入姓名'}
        self.fields['role'].label = '角色'
        self.fields['is_active'].label = '状态'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('密码必须大于6位')
        return password


class RoleListForm(forms.ModelForm):
    class Meta:
        model = Role
        exclude = ('id',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'permission':forms.SelectMultiple(attrs={'class':'form-control',
                                                     'size':'10',
                                                     'multiple':'multiple'}),
            'monment':forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(RoleListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label = '名称'
        self.fields['name'].errror_messages = {'required','请输入角色名称'}
        self.fields['permission'].label = 'URL'
        self.fields['permission'].required = False


class PermissionListForm(forms.ModelForm):
    class Meta:
        model = Permission
        exclude = ('id',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'url': forms.URLInput(attrs={'class':'form-control'}),
        }

    def __init__(self,*args,**kwargs):
        super(PermissionListForm,self).__init__(*args,**kwargs)
        self.fields['name'].label = '名称'
        self.fields['name'].error_messages = {'required':"请输入权限名称"}
        self.fields['url'].label = 'URL'
        self.fields['url'].error_messages = {'required':'请输入URL'}
