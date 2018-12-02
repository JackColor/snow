# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 下午4:12
# @Author  : JackColor
# @File    : discovery.py
import re
from collections import OrderedDict

from django.utils.module_loading import import_string
from django.conf import settings
from django.urls import URLResolver


def exclude_discover_url(url):
    """

    :param url:
    :return:
    """
    for i in settings.EXCLUDE_DISCOVEY_URL:
        if re.match(i, url):
            return True


def depth_discover_urls(pre_namespace, url_params, urlpatterns, order_url_dict):
    """

    :param pre_namespace:
    :param url_params:
    :param urlpatterns:
    :param order_url_dict:
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespance = "{0}:{1}".format(pre_namespace, item.namespace)
                else:
                    namespance = pre_namespace
            else:
                if item.namespace:
                    namespance = item.namespace
                else:
                    namespance = None
            depth_discover_urls(namespance, url_params + str(item.pattern), item.url_patterns, order_url_dict)
        else:
            if pre_namespace:
                name = "{0}:{1}".format(pre_namespace, item.name)
            else:
                name = item.name
            if not item.name:
                continue
            url = url_params + str(item.pattern)
            url = url.replace('^', '').replace('$', '')
            flag = exclude_discover_url(url)
            if flag:
                continue
            order_url_dict[name] = {'url_name': name, 'allow_url': url}

    return order_url_dict


def get_all_url_dict():
    """

    :return:
    """
    order_url_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    depth_discover_urls(None, "/", md.urlpatterns, order_url_dict)

    return order_url_dict
