# Generated by Django 4.0.2 on 2023-02-27 02:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0025_delete_netgraph'),
    ]

    operations = [
        migrations.CreateModel(
            name='Networkgraph',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
