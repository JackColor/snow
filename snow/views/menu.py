# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午8:14
# @Author  : JackColor
# @File    : menu.py

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse

from snow.commons.reverse import reverse_url
from snow.models import Menu, Permission
from snow.forms.menu import MenuFrom, PermissionFrom, LastPermissionFrom


def menu_list(request):
    menus = Menu.objects.all()
    current_id = request.GET.get("mid")
    cid = request.GET.get("cid")

    # 二级权限
    second_menus = Permission.objects.filter(meun_id=current_id)

    current_id = current_id if Menu.objects.filter(pk=current_id).exists() else None
    if not current_id:
        second_menus = []
    # 三级权限表
    last_menus = Permission.objects.filter(pid=cid)
    if not cid:
        last_menus = []
    if not current_id:
        last_menus = []

    cid = cid if Permission.objects.filter(pk=cid).exists() else None

    return render(request, "snow/body.html", locals())


def menu_edit(request, pk):
    obj = Menu.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse("菜单不存在")
    form = MenuFrom(instance=obj)
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = MenuFrom(instance=obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


def menu_add(request):
    form = MenuFrom()
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = MenuFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


@csrf_exempt
def menu_del(request, pk):
    url = reverse_url(request)
    if request.method == "GET":
        return render(request, "snow/delete.html", {"cancel": url})
    Menu.objects.filter(pk=pk).delete()
    return redirect(url)


def next_menu_add(request, first_id):
    print(first_id)
    menu_obj = Menu.objects.filter(pk=first_id).first()
    if not menu_obj:
        return HttpResponse("菜单不存在 ")
    form = PermissionFrom(initial={"meun": menu_obj})
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = PermissionFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


@csrf_exempt
def next_menu_del(request, pk):
    url = reverse_url(request)
    if request.method == "GET":
        return render(request, "snow/delete.html", {"cancel": url})
    Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def next_menu_edit(request, pk):
    permisson_obj = Permission.objects.filter(pk=pk).first()
    if not permisson_obj:
        return HttpResponse("二级菜单不存在 ")
    form = PermissionFrom(instance=permisson_obj)
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = PermissionFrom(request.POST, instance=permisson_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


def last_menu_add(request, last_id):
    """
    :param request:
    :param last_id:
    :return:
    """

    form = LastPermissionFrom()
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = LastPermissionFrom(request.POST)
        if form.is_valid():
            permission_obj = Permission.objects.filter(pk=last_id).first()
            if not permission_obj:
                return HttpResponse(" 权限菜单不存在", status=404)
            form.instance.pid = permission_obj
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


def last_menu_edit(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    permisson_obj = Permission.objects.filter(pk=pk).first()
    if not permisson_obj:
        return HttpResponse("权限不存在 ")
    form = LastPermissionFrom(instance=permisson_obj)
    if request.method == "GET":
        return render(request, "snow/change.html", {"form": form})
    else:
        form = LastPermissionFrom(request.POST, instance=permisson_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse_url(request))
    return render(request, "snow/change.html", {"form": form})


@csrf_exempt
def last_menu_del(request, pk):
    url = reverse_url(request)
    if request.method == "GET":
        return render(request, "snow/delete.html", {"cancel": url})
    Permission.objects.filter(pk=pk).delete()
    return redirect(url)
