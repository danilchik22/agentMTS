# Generated by Django 3.2.16 on 2023-01-12 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_auto_20230111_1304"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="work",
            name="user_of_promo",
        ),
    ]
