from email.policy import default
from django.db import models
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Service_Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "service_category"


class Service(models.Model):
    class ServiceType(models.TextChoices):
        BEAUTY = "Beauty"
        WELLNESS = "Wellness"

    class PaymentOption(models.TextChoices):
        EFTCard = "EFT-Card-Cash"
        CASH = "Cash"

    category = models.ForeignKey(
        Service_Category, related_name="services", on_delete=models.CASCADE)
    # remove type and add onSale bolean varibles
    type = models.CharField(
        max_length=10, choices=ServiceType.choices, default=ServiceType.WELLNESS
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    location_requirements = models.TextField(null=True)
    image1 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image3 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    duration = models.DurationField()
    promo_price = models.IntegerField()
    featured = models.IntegerField(default=0)
    price = models.IntegerField()
    max_recipients = models.IntegerField()
    payment_options = models.CharField(
        max_length=20, choices=PaymentOption.choices, default=PaymentOption.EFTCard)
    status = models.CharField(
        max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "service"
        db_table = "mobile_service"
        order_with_respect_to = "type"
