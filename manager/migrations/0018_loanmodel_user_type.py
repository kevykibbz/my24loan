# Generated by Django 3.2.9 on 2022-07-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_suggestionform_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanmodel',
            name='user_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
