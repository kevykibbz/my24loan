# Generated by Django 3.2.9 on 2022-07-26 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0034_auto_20220726_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardmodel',
            name='discount',
            field=models.IntegerField(blank=True, default=5, max_length=100, null=True),
        ),
    ]
