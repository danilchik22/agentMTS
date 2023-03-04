# Generated by Django 3.2.16 on 2023-01-12 16:03

from django.db import migrations, models
import mainapp.models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0005_alter_address_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={
                "verbose_name": "Адрес где кидал",
                "verbose_name_plural": "Adresses",
            },
        ),
        migrations.AlterField(
            model_name="work",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=mainapp.models.photo_house,
                verbose_name="фотки чужих листиков",
            ),
        ),
    ]