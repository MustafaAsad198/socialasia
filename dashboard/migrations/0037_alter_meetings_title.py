# Generated by Django 4.0.2 on 2024-02-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_meetings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='title',
            field=models.CharField(default='Untitled Meeting', max_length=200),
        ),
    ]
