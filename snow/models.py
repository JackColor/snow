from django.db import models
from django.core.validators import EmailValidator


class UserInfo(models.Model):
    """权限 use 表"""
    username = models.CharField(max_length=32, verbose_name="用户名称")
    password = models.CharField(max_length=16, verbose_name="密码")
    email = models.CharField(max_length=64, validators=(EmailValidator,), verbose_name="邮箱")
    roles = models.ManyToManyField(to="Role", verbose_name="角色")

    def __str__(self):
        return self.username


class Role(models.Model):
    """角色表"""
    title = models.CharField(max_length=16, verbose_name="角色名称")
    permissons = models.ManyToManyField(to="Permission", blank=True, verbose_name="权限")

    def __str__(self):
        return self.title


class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=16, verbose_name="权限名称", unique=True)
    allow_url = models.CharField(max_length=256, verbose_name="权限url")

    pid = models.ForeignKey(verbose_name="关联父菜单", to="self", related_name="parents", help_text="与哪一个菜单栏关联",
                            on_delete=models.CASCADE, null=True, blank=True)
    url_name = models.CharField(verbose_name="url别名", null=True, blank=True, max_length=32)
    meun = models.ForeignKey(to="Menu", on_delete=models.CASCADE, verbose_name="子菜单", null=True, blank=True,
                             help_text="null不可作为菜单,说白了就是只能在body里面展示，能不能出现在菜单栏")

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField("一级菜单名称", max_length=32)
    icon = models.CharField("标签", max_length=64, )

    def __str__(self):
        return self.title
