from django.core.validators import RegexValidator
from django.forms import CharField
from django.core.exceptions import ValidationError
import re

class PhoneField(CharField):
    default_validators = [RegexValidator(regex="^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$")]
    def __init__(self,**kwargs):
        super().__init__(strip=True,**kwargs)
