# Generated by Django 3.2.9 on 2021-11-20 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0008_rename_email_citizen_cemail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citizen',
            old_name='cemail',
            new_name='email',
        ),
    ]
