# Generated by Django 4.0.6 on 2022-08-02 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]