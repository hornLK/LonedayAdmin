from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.
# access auth user table
class AccessUser(models.Model):
    username = models.CharField(max_length=64,unique=True,db_index=True,blank=True)
    email = models.EmailField(max_length=255,unique=True,db_index=True)
    accessuser_id = models.IntegerField(db_index=True,null=True,blank=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return "Access用户: %s" % self.username
    class Meta:
        verbose_name = "access用户表"
        verbose_name_plural = "access用户表"
    
#permission  table
class Permission(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField(max_length=255)

    def __str__(self):
        return '%s(%s)' % (self.name,self.url)
    class Meta:
        verbose_name = "权限信息表"
        verbose_name_plural = "权限信息表"

#role table
class Role(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(Permission,blank=True)
    monment = models.TextField(blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "角色信息表"
        verbose_name_plural = "角色信息表"

class UserManager(BaseUserManager):
    def create_user(self,email,nickname,password=None):
        if not nickname:
            raise ValueError('用户姓名必须录入')

        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,nickname,password):
        user = self.create_user(email,
                                nickname=nickname,
                                password=password,)
        user.is_activae = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def email_to_username(self,email):
        username = email.split("@")[0].replace('.','_')
        return username

class UserInfo(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True,db_index=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64,null=True)
    role = models.ForeignKey(Role,null=True,blank=True,on_delete=models.SET_NULL)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname',]

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self,app_label):
        return True

    def get_short_name(self):
        return self.email.split("@")[0].replace('.','_')

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        verbose_name = "登录用户信息表"
        verbose_name_plural = "登录用户信息表"
