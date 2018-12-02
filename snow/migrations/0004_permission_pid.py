# Generated by Django 2.0 on 2018-12-01 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snow', '0003_auto_20181201_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='pid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='snow.Permission', verbose_name='关联父菜单'),
        ),
    ]
