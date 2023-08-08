# Generated by Django 4.0.2 on 2023-08-08 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_caption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examplecaption',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True)),
                ('contentlength', models.PositiveIntegerField(choices=[(11, 'Long'), (12, 'Medium'), (13, 'Short')], default=11)),
                ('obj', models.PositiveIntegerField(blank=True, choices=[(61, 'Mountain'), (62, 'Street'), (63, 'Glacier'), (64, 'Building'), (65, 'Sea'), (66, 'Forest')], null=True)),
            ],
        ),
    ]
