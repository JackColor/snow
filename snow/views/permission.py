# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 下午8:09
# @Author  : JackColor
# @File    : permission.py
from collections import OrderedDict

from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import reverse
from django.forms import formset_factory
from django.db.utils import IntegrityError

from snow import models
from snow.commons.discovery import get_all_url_dict
from django.views.decorators.csrf import csrf_exempt
from snow.forms.permission import PermissionForm, UpdatePermissonFrom


def multi_permissions(request):
    """

    all_url_dict =  {
    snow:role_list:{'url_name': 'snow:role_list', 'allow_url': '/snow/role/list/'},
    snow:role_add :{'url_name': 'snow:role_add', 'allow_url': '/snow/role/add/'}
    }


    :param request:
    :return:
    """
    create_forms = None
    update_forms = None
    create_form_cls = formset_factory(PermissionForm, extra=0)
    update_form_cls = formset_factory(UpdatePermissonFrom, extra=0)
    action_type = request.GET.get("type")
    # 批量增加
    if request.method == "POST" and action_type == "create":
        """添加"""
        create_forms = create_form_cls(request.POST)
        if create_forms.is_valid():
            permission_obj_list = []
            has_errors = False
            post_data = create_forms.cleaned_data
            for i in range(0, create_forms.total_form_count()):
                row_data = post_data[i]
                try:
                    permission_obj = models.Permission(**row_data)
                    permission_obj.validate_unique()  #
                    permission_obj_list.append(permission_obj)
                except Exception as e:
                    has_errors = True
                    create_forms.errors[i].update(e)
            if not has_errors:
                try:
                    models.Permission.objects.bulk_create(permission_obj_list, batch_size=100)
                except IntegrityError:
                    create_forms.msg = "请检查名称是否规范( 名称重复 或其他 )"
                else:
                    create_forms = None
    # 批量更新
    if request.method == "POST" and action_type == "update":
        """批量更新"""
        update_forms = update_form_cls(request.POST)
        if update_forms.is_valid():
            update_data = update_forms.cleaned_data
            update_has_errors = False
            for i in range(0, update_forms.total_form_count()):
                update_row = update_data[i]
                pk = update_row.pop("id")
                update_permission_obj = models.Permission.objects.filter(pk=pk).first()  # type: models.Permission
                for name, val in update_row.items():
                    setattr(update_permission_obj, name, val)
                    try:
                        update_permission_obj.validate_unique()
                        update_permission_obj.save()
                    except Exception as e:
                        update_forms.errors[i].update(e)
                        update_has_errors = True
                if not update_has_errors:
                    update_forms = None

    # 发现项目中的所有路由
    all_url_dict = get_all_url_dict()

    all_url_set = set(all_url_dict.keys())

    # 数据库里面的所以路由信息

    database_url_dict_list = models.Permission.objects.all().values("id", "title",
                                                                    "allow_url", "url_name",
                                                                    "meun_id", "pid_id")
    database_url_dict = OrderedDict()
    database_url_set = set()
    for item in database_url_dict_list:
        database_url_dict[item["url_name"]] = item
        database_url_set.add(item["url_name"])

    # 判断 两个 dict 不一致
    for name, item in database_url_dict.items():

        existed_key = all_url_dict.get(name)  # 路由发现的dict
        if not existed_key:
            continue
        if item["allow_url"] != existed_key["allow_url"]:
            item["allow_url"] = "数据与发现URL 不一致"

    # 需要在数据可创建的url 路由多
    create_url_set = all_url_set - database_url_set

    # 没有创建 create_from get 方法
    if not create_forms:
        create_form_cls = formset_factory(PermissionForm, extra=0)
        create_forms = create_form_cls(initial=[
            item for name, item in all_url_dict.items() if name in create_url_set
        ])

    # 需要删除的url  数据库 多
    detele_url_set = database_url_set - all_url_set

    delete_url_dict = [item for name, item in database_url_dict.items() if name in detele_url_set]

    # 更新的 url
    update_url_set = database_url_set & all_url_set  # 交集

    if not update_forms:
        update_form_cls = formset_factory(UpdatePermissonFrom, extra=0)
        update_forms = update_form_cls(initial=[
            item for name, item in database_url_dict.items() if name in update_url_set])

    return render(request,
                  'snow/multi_permisson.html',
                  {"create_forms": create_forms,
                   "delete_dict": delete_url_dict,
                   "update_forms": update_forms,
                   }
                  )


@csrf_exempt
def multi_permissions_del(request, pk):
    url = reverse("snow:multi_permissions")
    if request.method == "GET":
        return render(request, "snow/delete.html", {"cancel": url})
    models.Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def distribute_permissions(reuqest):
    # 用户列表
    uid = reuqest.GET.get("uid")
    rid = reuqest.GET.get("rid")
    user_roles_id_dict = {}
    permissions_id_dict = {}
    all_menu_dict = {}
    all_second_menu_dict = {}
    if reuqest.method == "POST" and reuqest.POST.get("type") == "roles" and uid:
        user_obj = models.UserInfo.objects.filter(id=uid).first()
        if not user_obj:
            return HttpResponse("操作不正确!")  # TODO errors.html
        roles_id = reuqest.POST.getlist("roles")
        user_obj.roles.set(roles_id)

    if reuqest.method == "POST" and reuqest.POST.get("type") == "permission" and rid:
        role_obj = models.Role.objects.filter(pk=rid).first()  # type:models.Role
        if not role_obj:
            return HttpResponse("errors")
        permissions_id = reuqest.POST.getlist("permissions")
        role_obj.permissons.set(permissions_id)

    if uid:
        user_obj = models.UserInfo.objects.filter(id=uid).first()  # type: models.UserInfo
        if user_obj:
            user_roles_id_dict = {row["id"]: None for row in user_obj.roles.all().values("id")}
            user_permissions = user_obj.roles.filter(permissons__id__isnull=False).values("permissons__id").distinct()
            permissions_id_dict = {row["permissons__id"]: None for row in user_permissions}
        else:
            uid = None

    if rid:
        role = models.Role.objects.filter(id=rid)
        if role:
            role_permissions = role.filter(permissons__id__isnull=False).values("permissons__id").distinct()
            permissions_id_dict = {row["permissons__id"]: None for row in role_permissions}
        else:
            rid = None

    # 所有用户信息
    all_user_list = models.UserInfo.objects.all()
    # 所有 角色信息
    all_roles_list = models.Role.objects.all()

    # 菜单信息 用于后面的 数据结构展示
    all_menu_list = models.Menu.objects.all().values("id", "title")

    all_second_menu_list = models.Permission.objects.filter(meun__isnull=False).values("id", "title", "meun_id")

    all_permission_list = models.Permission.objects.filter(meun__isnull=True).values("id", "title", "pid_id")

    # 构造数据结构
    for item in all_menu_list:
        item["children"] = []
        all_menu_dict[item["id"]] = item

    for row in all_second_menu_list:
        meun_id = row["meun_id"]
        row["children"] = []
        all_second_menu_dict[row["id"]] = row
        all_menu_dict[meun_id]["children"].append(row)

    for row in all_permission_list:
        pid = row["pid_id"]
        if not pid:
            continue
        all_second_menu_dict[pid]["children"].append(row)

    return render(reuqest, "snow/distribute_permissions.html",
                  {"all_user_list": all_user_list,
                   "all_menu_list": all_menu_list,
                   "all_roles_list": all_roles_list,
                   "user_roles_id_dict": user_roles_id_dict,
                   "permissions_id_dict": permissions_id_dict,
                   "rid": rid,
                   "uid": uid,
                   }
                  )
