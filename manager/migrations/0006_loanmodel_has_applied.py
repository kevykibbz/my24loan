# Generated by Django 3.2.9 on 2022-07-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_loanmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='has_applied',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
