# Generated by Django 5.0.2 on 2024-02-26 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminUI', '0016_jobsdb_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marquee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
