# Generated by Django 3.2.9 on 2022-07-26 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0033_loanmodel_bank_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanmodel',
            name='page_status',
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='is_new',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loanmodel',
            name='signature_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
