# Generated by Django 3.2.7 on 2021-10-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20211001_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='date',
            field=models.DateTimeField(verbose_name='%Y-%m-%d'),
        ),
    ]
