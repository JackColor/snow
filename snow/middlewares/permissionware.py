# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 上午11:10
# @Author  : JackColor
# @File    : permissionware.py
import re
from django.conf import settings
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class PermissionWare(MiddlewareMixin):

    def process_request(self, request):
        current_url = request.path_info
        for url in settings.VALIDATE_URL:  # 白名单
            if re.match(url, current_url):
                return
        # 权限url
        permission_url_dict = request.session.get(settings.PERMISSION_KEY)
        # 动态 添加 移除 from redis 某人的 权限url
        if not permission_url_dict:
            return HttpResponse("先登录，或未分配任何权限")
        flag = False

        # TODO 对不同页面需要直接访问不做限制

        record_url = [{"title": "首页", "url": "#"}]
        for item in permission_url_dict.values():
            regx_url = '^{url}$'.format(url=item["url"])
            if re.match(regx_url, current_url):
                flag = True
                request.selected_url_id = item["pid"] or item["id"]
                if not item["pid"]:
                    record_url.append({"title": item["title"], "url": item["url"]})
                else:
                    record_url.append({"title": item["p_title"], "url": item["p_url"]})
                    record_url.append({"title": item["title"], "url": item["url"]})
                break

        request.breadcrumb_list = record_url

        # from pprint import pprint
        # pprint(permission_url_dict)
        if not flag:
            return HttpResponse("无权限")
