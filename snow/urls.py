from django.conf.urls import url
from snow.views import roles, menu, permission

app_name = "snow"

urlpatterns = [
    # role 角色
    url(r'^role/list/$', roles.role_list, name="role_list"),
    url(r'^role/add/$', roles.role_add, name="role_add"),
    url(r'^role/edit/(?P<pk>\d+)$', roles.role_edit, name="role_edit"),
    url(r'^role/del/(?P<pk>\d+)$', roles.role_del, name="role_del"),

    # menu 菜单
    url(r'^menu/list/$', menu.menu_list, name="menu_list"),
    url(r'^menu/add/$', menu.menu_add, name="menu_add"),
    url(r'^menu/delete/(?P<pk>\d+)/$', menu.menu_del, name="menu_del"),
    url(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name="menu_edit"),

    # menu 二级菜单

    url(r'^next_menu/add/(?P<first_id>\d+)/$', menu.next_menu_add, name="next_menu_add"),
    url(r'^next_menu/del/(?P<pk>\d+)/$', menu.next_menu_del, name="next_menu_del"),
    url(r'^next_menu/edit/(?P<pk>\d+)/$', menu.next_menu_edit, name="next_menu_edit"),

    # 权限菜单

    url(r'^last_menu/add/(?P<last_id>\d+)/$', menu.last_menu_add, name="last_menu_add"),
    url(r'^last_menu/edit/(?P<pk>\d+)/$', menu.last_menu_edit, name="last_menu_edit"),
    url(r'^last_menu/del/(?P<pk>\d+)/$', menu.last_menu_del, name="last_menu_del"),

    # 发现路由 路由操作
    url(r'^discovery/url/$', permission.multi_permissions, name="multi_permissions"),
    url(r'^discovery/url/del/(?P<pk>\d+)$', permission.multi_permissions_del, name="multi_permissions_del"),

    # 权限分配
    url(r'^distribute/permission/$', permission.distribute_permissions, name="distribute_permissions"),

]
