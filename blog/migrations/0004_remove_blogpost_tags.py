# Generated by Django 5.1.1 on 2024-10-07 08:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_alter_profile_profile_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blogpost",
            name="tags",
        ),
    ]
