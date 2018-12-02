# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 上午11:33
# @Author  : JackColor
# @File    : permission.py
from django.conf import settings
from snow.models import UserInfo


def init_permission(user: UserInfo, request):
    queryset = user.roles.filter(permissons__allow_url__isnull=False).values(
        "permissons__allow_url", "permissons__title",
        "permissons__meun_id", "permissons__meun__title",
        "permissons__meun__icon", "permissons__id",
        "permissons__pid_id", "permissons__pid__title",
        "permissons__pid__allow_url", "permissons__url_name"
    ).distinct()
    permission_url_dict = dict()
    menu_dict = dict()
    for permission in queryset:
        # 注册权限 url 到 permission_url_list
        permission_url_dict[permission["permissons__url_name"]] = {
            "title": permission.get("permissons__title"),
            "url": permission.get("permissons__allow_url"),
            "id": permission.get("permissons__id"),
            # 父亲的 title 与 url
            "pid": permission.get("permissons__pid_id"),
            "p_title": permission.get("permissons__pid__title"),
            "p_url": permission.get("permissons__pid__allow_url")
        }

        menu_id = permission.get("permissons__meun_id")
        if menu_id:
            # 注册 node 孩子到 menu_dict
            node = {"id": permission.get("permissons__id"), "url": permission.get("permissons__allow_url"),
                    "name": permission.get("permissons__title")}
            if menu_id in menu_dict:
                menu_dict[menu_id]["children"].append(node)
            else:
                menu_dict[menu_id] = {
                    "title": permission.get("permissons__meun__title"),
                    "icon": permission.get("permissons__meun__icon"),
                    "children": [node, ]
                }

    # print("---->", permission_url_dict)
    request.session[settings.PERMISSION_KEY] = permission_url_dict

    request.session[settings.MENU_KEY] = menu_dict
    username = user.username
    request.session["user"] = username
