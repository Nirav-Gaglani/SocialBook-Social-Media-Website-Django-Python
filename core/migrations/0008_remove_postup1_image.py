# Generated by Django 4.0.6 on 2022-08-02 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_postup1_delete_postup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postup1',
            name='image',
        ),
    ]