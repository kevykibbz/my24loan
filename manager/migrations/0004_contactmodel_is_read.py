# Generated by Django 3.2.9 on 2022-07-09 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_contactmodel_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmodel',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]