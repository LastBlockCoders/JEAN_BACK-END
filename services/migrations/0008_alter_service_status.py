# Generated by Django 4.1.1 on 2022-11-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_alter_service_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(max_length=255),
        ),
    ]