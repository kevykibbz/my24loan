# Generated by Django 3.2.9 on 2022-07-09 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20220709_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
