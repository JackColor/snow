# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午11:53
# @Author  : JackColor
# @File    : reverse.py
from django.urls import reverse
from django.http.request import QueryDict


def reverse_url(request):
    url = reverse("snow:menu_list")
    origin_params = request.GET.get("_filter")
    if origin_params:
        url = "%s?%s" % (url, origin_params)
    return url


def save_url(request, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)
    if request.GET:
        origin_dict = QueryDict(mutable=True)
        origin_dict["_filter"] = request.GET.urlencode()
        url = "{url}?{params}".format(url=url, params=origin_dict.urlencode())

    return url
