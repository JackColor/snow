# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 上午10:38
# @Author  : JackColor
# @File    : validate.py


def validate_exist(model, nid):
    """

    :param model:
    :param nid:
    :return:
    """
    return nid if model.objects.filter(pk=nid).exists() else None
