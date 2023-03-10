# Generated by Django 4.0.2 on 2023-02-27 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0023_alter_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Netgraph',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.PositiveIntegerField(default=1)),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
