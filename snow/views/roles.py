# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午6:05
# @Author  : JackColor
# @File    : roles.py
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, reverse, HttpResponse

from snow.forms.roles import RoleForm
from snow.models import Role
from snow.commons.reverse import reverse_url


def role_list(request):
    roles = Role.objects.all()
    return render(request, "snow/role_list.html", locals())


def role_add(request):
    form = RoleForm()

    if request.method == "POST":

        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("snow:role_list"))

    return render(request, "snow/change.html", {"form": form})


def role_edit(request, pk):
    role_obj = Role.objects.filter(pk=pk).first()

    form = RoleForm(instance=role_obj)
    if request.method == "POST":
        form = RoleForm(instance=role_obj, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("snow:role_list"))

    return render(request, "snow/change.html", {"form": form})


@csrf_exempt
def role_del(request, pk):
    url = reverse("snow:role_list")
    if request.method == "GET":
        return render(request, "snow/delete.html", {"cancel": url})
    Role.objects.filter(pk=pk).delete()
    return redirect(url)
