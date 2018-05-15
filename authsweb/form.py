from django.forms import CharField, EmailField, IntegerField, ChoiceField
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import PasswordInput, Textarea, TextInput, EmailInput
from utils.request_api import secret_apirequest


class AddUserForm(forms.Form):
    email = EmailField(required=True,
                      widget=EmailInput(attrs={
                        "class":"form-control",
                        "placeholder":"公司邮箱",
                        "value":"",
                        "required":"required"
                      }))
    chinese = CharField(required=True,
                         max_length = 32,
                        widget=TextInput(attrs={
                            "class":"form-control",
                            "placeholder":"中文名",
                            "value":"",
                            "required":"required"
                        }))
    phonenumber = CharField(required=True,
                            validators=[RegexValidator(regex=r'^[0-9][0-9]+$',
                                                      message="请输入正确的手机号",
                                                      code="invalid"),],
                            max_length = 11,
                            min_length = 11,
                            widget=TextInput(attrs={
                            "class":"form-control",
                            "placeholder":"手机号",
                            "value":"",
                            "required":"required",
                            "data-inputmask":"'mask':['999-9999-9999','+099 99 99 9999[9]-9999']",
                                "data-mask":""
                           }))

