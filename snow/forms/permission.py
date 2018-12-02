# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 下午8:29
# @Author  : JackColor
# @File    : permission.py
from django import forms
from snow import models


class PermissionForm(forms.Form):
    title = forms.CharField(max_length=32, widget=forms.TextInput(attrs={"class": "form-control"}))

    allow_url = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    url_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    meun_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["meun_id"].choices += models.Menu.objects.values_list('id', 'title')
        # 菜单 tab
        self.fields["pid_id"].choices += models.Permission.objects. \
            filter(pid__isnull=True).exclude(meun__isnull=True).values_list('id', 'title')


class UpdatePermissonFrom(PermissionForm):
    id = forms.IntegerField(widget=forms.HiddenInput())
