# Generated by Django 3.2.9 on 2021-11-24 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0009_rename_cemail_citizen_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='comp_pic',
            field=models.FileField(blank=True, null=True, upload_to='complain/'),
        ),
    ]
