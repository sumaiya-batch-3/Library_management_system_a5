# Generated by Django 4.2.4 on 2024-03-25 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_publisherinfo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisherinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user/media/uploads/'),
        ),
    ]
