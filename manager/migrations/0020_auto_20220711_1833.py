# Generated by Django 3.2.9 on 2022-07-11 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_auto_20220710_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanmodel',
            name='address',
        ),
        migrations.RemoveField(
            model_name='loanmodel',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='loanmodel',
            name='credit_limit',
        ),
        migrations.AlterField(
            model_name='extendedauthuser',
            name='company',
            field=models.CharField(blank=True, default='My24loan', max_length=100, null=True),
        ),
    ]
