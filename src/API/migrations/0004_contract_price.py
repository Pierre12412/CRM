# Generated by Django 3.2.7 on 2021-09-30 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_event_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='price',
            field=models.IntegerField(default=None),
        ),
    ]
