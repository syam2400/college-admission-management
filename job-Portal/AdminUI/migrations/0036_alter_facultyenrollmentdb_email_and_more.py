# Generated by Django 4.2.7 on 2024-04-05 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminUI', '0035_facultyenrollmentdb_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facultyenrollmentdb',
            name='Email',
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='studentdb',
            name='Email',
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]