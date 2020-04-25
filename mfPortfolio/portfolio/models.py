from django.db import models
# Create your models here.

class MutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    mf_name = models.CharField(max_length=256)
    holdings_url = models.CharField(max_length=512)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
