# Generated by Django 3.2.7 on 2021-09-29 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20210929_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='Titre', max_length=50),
            preserve_default=False,
        ),
    ]