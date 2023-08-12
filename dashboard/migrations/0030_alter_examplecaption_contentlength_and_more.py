# Generated by Django 4.0.2 on 2023-08-09 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_remove_caption_contentlength'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examplecaption',
            name='contentlength',
            field=models.PositiveIntegerField(choices=[(11, 'Long'), (12, 'Medium'), (13, 'Short')]),
        ),
        migrations.AlterField(
            model_name='examplecaption',
            name='obj',
            field=models.PositiveIntegerField(choices=[(61, 'Mountain'), (62, 'Street'), (63, 'Glacier'), (64, 'Building'), (65, 'Sea'), (66, 'Forest')]),
        ),
        migrations.AlterField(
            model_name='examplecaption',
            name='text',
            field=models.TextField(),
        ),
    ]