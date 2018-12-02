# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 上午9:08
# @Author  : JackColor
# @File    : basefrom.py

from django import forms


class BoostrapForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
