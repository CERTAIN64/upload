# Generated by Django 3.2.9 on 2021-11-16 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citizen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FIR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('dis', models.TextField()),
                ('fir_at', models.DateField()),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('fir_pic', models.FileField(blank=True, null=True, upload_to='FIR/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citizen.citizen')),
            ],
        ),
    ]