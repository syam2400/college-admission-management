# Generated by Django 4.2.7 on 2023-11-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminUI', '0009_jobsdb_image_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='JnewsDB',
            fields=[
                ('newsId', models.AutoField(primary_key=True, serialize=False)),
                ('news_Title', models.CharField(blank=True, max_length=100, null=True)),
                ('news_Location', models.CharField(blank=True, max_length=100, null=True)),
                ('news_date', models.DateField(blank=True, null=True)),
                ('Description', models.CharField(blank=True, max_length=1000, null=True)),
                ('news_image', models.ImageField(blank=True, null=True, upload_to='job')),
            ],
        ),
    ]
