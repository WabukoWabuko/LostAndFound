# Generated by Django 4.2.19 on 2025-03-01 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_remove_item_image_item_images'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
