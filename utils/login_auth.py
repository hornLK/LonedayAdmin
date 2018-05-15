from functools import wraps
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
import json

def login_auth(func):
    @wraps(func)
    def decorated_function(request,*args,**kwargs):
        result = request.session.get("auth_user",None)
        if not result:
            login_url = reverse("webLogin")
            return HttpResponseRedirect(login_url)
        result = json.loads(result)
        request.username = result['username']
        response = func(request,*args,**kwargs)
        return response
    return decorated_function

