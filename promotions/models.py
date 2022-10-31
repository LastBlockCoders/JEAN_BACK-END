from django.db import models

# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=25)
    description = models.TextField()
    amount = models.IntegerField()
    once_off = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    expiry = models.DateField()
    user_id = models.BigIntegerField()
