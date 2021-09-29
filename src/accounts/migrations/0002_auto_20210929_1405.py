# Generated by Django 3.2.7 on 2021-09-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='permission',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Support'), (3, 'Sales'), (4, 'Admin')], default=None),
            preserve_default=False,
        ),
    ]
