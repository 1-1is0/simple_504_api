# Generated by Django 5.0.2 on 2024-05-08 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0006_alter_unitmodel_options_unitmodel_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='unitmodel',
            name='image',
            field=models.ImageField(blank=True, upload_to='unit_images/', verbose_name='image'),
        ),
    ]
