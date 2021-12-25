# Generated by Django 4.0 on 2021-12-25 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='The url which is encoded in the QRCode', max_length=1024, unique=True, verbose_name='Adresse (URL)')),
                ('location_id_hash', models.BinaryField(help_text='SHA256 hash of the CWA location ID', verbose_name='Location ID Hash')),
            ],
        ),
    ]
