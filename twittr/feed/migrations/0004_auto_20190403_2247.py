# Generated by Django 2.1.7 on 2019-04-04 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20190403_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(max_length=280),
        ),
    ]
