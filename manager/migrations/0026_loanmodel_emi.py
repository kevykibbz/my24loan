# Generated by Django 3.2.9 on 2022-07-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0025_cardmodel_loan_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='emi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
