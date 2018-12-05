# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午12:37
# @Author  : JackColor
# @File    : snow.py

from collections import OrderedDict
from django.template import Library
from django.conf import settings
from snow.commons.reverse import save_url

register = Library()


@register.inclusion_tag("snow/meun.html")
def menu_list(request):
    """"""
    menu_dict = request.session.get(settings.MENU_KEY)
    order_meun_dict = OrderedDict()
    for index, item in menu_dict.items():
        item["cls"] = "hide"
        for chl in item["children"]:
            if chl["id"] == request.selected_url_id:
                item["cls"] = ""
                chl["act"] = "active"
        order_meun_dict[index] = item

    return {"menu_dict": order_meun_dict, "path_info": request.path_info}


@register.inclusion_tag("snow/breadcrumb.html")
def breadcrumb(request):
    """
    :param request:
    :return:
    """
    return {"breadcrumb_list": request.breadcrumb_list}


@register.filter()
def has_permission(request, name):
    return name in request.session[settings.PERMISSION_KEY]


@register.simple_tag
def exist_url(request, name, *args, **kwargs):
    """
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    return save_url(request, name, *args, **kwargs)
