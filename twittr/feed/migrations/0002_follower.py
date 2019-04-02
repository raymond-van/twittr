# Generated by Django 2.1.7 on 2019-03-27 04:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m_follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]