# Generated by Django 4.1.1 on 2022-11-03 21:44

from django.db import migrations, models
import services.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_service_featured_service_promo_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_category',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=services.models.upload_to),
        ),
        migrations.AlterField(
            model_name='service_category',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]