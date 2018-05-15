from restorage.models import User

class BackendModelsAuth:
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def auth_account(self):
        try:
            user = User.objects.get(email=self.email)
            if user.verify_password(self.password):
                return True
            else:
                return False
        except User.DoesNotExist:
            return False

    def add_account(self):
        try:
            user = User.objects.get(email=email)
            return False
        except User.DoesNotExist:
            user = User(email=email)
            user.password=password
            return True

    def change_password(self):
        try:
            user = User.objects.get(email=email)
            user.password(password)
        except User.DoesNotExist:
            return False

class MiaoAccountAuth():
    pass

def auth_factory(email,password,authtype='model'):
    if authtype == "model":
        auth = BackendModelsAuth
    elif authtype == "account":
        auth = MiaoAccountAuth
    else:
        raise ValueError("not found auth type")
    return auth(email,password)

def auth_to(email,password,authtype="model"):
    factory = None
    try:
        factory = auth_factory(email,password,authtype="model")
    except ValueError as ve:
        print(ve)
    return factory
