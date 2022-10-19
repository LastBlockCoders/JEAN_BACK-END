# Generated by Django 4.1.1 on 2022-10-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='payment_options',
            field=models.CharField(choices=[('EFT/Card/Cash', 'Eftcard'), ('Cash', 'Cash')], default='EFT/Card/Cash', max_length=20),
        ),
        migrations.AlterField(
            model_name='service',
            name='location_requirements',
            field=models.TextField(null=True),
        ),
    ]