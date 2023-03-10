# Generated by Django 4.0.2 on 2023-02-08 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0017_delete_notofication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notofication',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('ntype', models.PositiveIntegerField(choices=[(91, 'FOllow'), (92, 'Message')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nfromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nfromuser', to=settings.AUTH_USER_MODEL)),
                ('ntouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
