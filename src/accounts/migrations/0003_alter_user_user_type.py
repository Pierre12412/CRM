# Generated by Django 3.2.7 on 2021-09-29 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210929_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Support'), (3, 'Sales'), (4, 'Admin')], null=True),
        ),
    ]
