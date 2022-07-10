# Generated by Django 3.2.9 on 2022-07-09 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_loanmodel_has_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='is_verfied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]