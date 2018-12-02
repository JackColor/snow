# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午6:05
# @Author  : JackColor
# @File    : roles.py
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from snow.models import Role


def role_list(request):
    roles = Role.objects.all()
    return render(request, "snow/role_list.html", locals())


def role_add(request):
    return HttpResponse("add")
