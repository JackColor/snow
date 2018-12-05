# -*- coding: utf-8 -*-
# @Time    : 2018/12/5 下午8:46
# @Author  : JackColor
# @File    : roles.py

from snow.forms import basefrom
from snow import models


class RoleForm(basefrom.BoostrapForm):
    class Meta:
        model = models.Role
        fields = ["title", ]
