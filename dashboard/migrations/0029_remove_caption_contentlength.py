# Generated by Django 4.0.2 on 2023-08-09 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_examplecaption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caption',
            name='contentlength',
        ),
    ]
