from django.db import models
from .utils.common_enums import AssetClass
# Create your models here.


class MutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    mf_name = models.CharField(max_length=256)
    holdings_url = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mf_name


