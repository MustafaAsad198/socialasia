# Generated by Django 4.0.2 on 2023-02-08 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0015_follow_requested'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notofication',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('ntype', models.PositiveIntegerField(choices=[(91, 'FOllow'), (92, 'Message')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('fromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
