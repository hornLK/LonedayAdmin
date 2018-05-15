from django.urls import path,re_path
from . import views
urlpatterns = [
    path('/index/',views.auths_index,name="auths_index"),
    #path('/auths_index/',views.auths_index,name="authss_index"),
    path('/authorizeuser/ajax/edituser/',views.authorizeEditUser,name="auths_edituser"),
    path('/authorizeuser/ajax/getroles/',views.authorizeGetRoles,name="auths_getroles"),
    path('/authorizeuser/ajax/deluserhost/',views.delUserHost,name="auths_deluserhost"),
    path('/authorizeuser/ajax/authhostsuser/',views.authorizeAuthHostsUser,name="auths_hostuser"),
    re_path('/authorizeuser/ajax/userouthosts/userpage-(?P<user_id>\d+)/',views.authorizeUserOutHosts,name="auths_userouthosts"),
    path('/authorizeuser/ajax/editrole/',views.authorizeEditUserRole,name="auths_editrole"),
    #re_path(r'/authorizeuser/adduserrole/userpage-(?P<user_id>\d+)/',views.authorizeAddUserRole,name="auths_adduserrole"),
    re_path(r'/authorizeuser/adduserrole/userpage-(?P<user_id>\d+)/',views.AuthsUserAddHosts,name="auths_adduserrole"),
    re_path(r'/authorizeuser/userpage-(?P<user_id>\d+)/',views.UserHosts,name="authorizeUser"),
    re_path(r'/authorizeuser/userdetail/',views.AuthsUserDetail,name="auths_userdetail"),
    #re_path(r'/user_hosts/user-(?P<user_id>\d)/',views.UserHosts,name="user_hosts"),
]
