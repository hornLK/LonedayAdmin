import datetime,json
import requests
from django.conf import settings
from .request_api import secret_apirequest
def email_sendkey(email,pubkey,prikey):
    mail_dict={
                "title": "登录跳板机密钥",
                "content":"您的跳板机密钥文件见附件",
                "receivers":[email,],
                "pub_key":pubkey,
                "pri_key":prikey
                }
    try:
        headers = secret_apirequest(settings.AUTHS_SECRETKEY)
        requests.post(url=settings.MAIL_API,headers=headers,data=json.dumps(mail_dict))
        return True
    except Exception as e:
        print(e)
        return False
