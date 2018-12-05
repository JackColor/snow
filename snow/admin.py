from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from snow.models import *
from webdemo import models

admin.site.register(models.Customer)
admin.site.register(models.Payment)


class PermissonConfig(ModelAdmin):
    # list_display = ["username", "roles"]

    list_display = ["title", "allow_url", ]


admin.site.register(UserInfo)
admin.site.register(Role)

admin.site.register(Permission, PermissonConfig)
