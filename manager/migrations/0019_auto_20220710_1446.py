# Generated by Django 3.2.9 on 2022-07-10 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_loanmodel_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='card_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='credit_limit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
