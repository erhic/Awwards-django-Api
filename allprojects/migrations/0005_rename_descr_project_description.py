# Generated by Django 4.0.3 on 2022-03-17 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allprojects', '0004_alter_project_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='descr',
            new_name='description',
        ),
    ]