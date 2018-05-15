import time,hashlib
def secret_apirequest(api_key):
    SECRET_API_KEY = api_key
    time_span = time.time()
    secret_data = "%s|%0.0f" % (SECRET_API_KEY,time_span)
    hash_obj = hashlib.md5(secret_data.encode("utf-8"))
    encryption = hash_obj.hexdigest()
    #header_secretkey = encryption+"|"+str(time_span)
    header_secretkey = "%s|%0.0f" % (encryption,time_span)
    headers = {'content-type':'application/json',"X-Http-Secretkey":header_secretkey}
    return headers

if __name__ == "__main__":
    a=secret_apirequest("123")
    print(a)
