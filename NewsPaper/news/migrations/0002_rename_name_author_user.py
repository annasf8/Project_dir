# Generated by Django 4.2.1 on 2023-07-01 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='user',
        ),
    ]
