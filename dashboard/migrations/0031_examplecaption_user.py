# Generated by Django 4.0.2 on 2023-08-10 04:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0030_alter_examplecaption_contentlength_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examplecaption',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
