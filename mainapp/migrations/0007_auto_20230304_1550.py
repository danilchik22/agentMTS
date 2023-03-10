# Generated by Django 3.2.16 on 2023-03-04 15:50

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20230112_1603'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Adress of work', 'verbose_name_plural': 'Adresses'},
        ),
        migrations.AlterField(
            model_name='work',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=mainapp.models.photo_house, verbose_name='Photo of ad'),
        ),
    ]
