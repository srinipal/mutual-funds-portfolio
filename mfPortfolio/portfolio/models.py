from django.db import models
from datetime import datetime

from .utils.common_enums import SIPFrequency
from mutualFund.models import MutualFund as MutualFundGlobal


class MutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund_global = models.ForeignKey(MutualFundGlobal, verbose_name='Mutual Fund', related_name='investments', on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    last_transaction_date = models.DateField(auto_now=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.mutual_fund_global.mf_name


class MutualFundSIP(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    mutual_fund = models.ForeignKey(MutualFund, verbose_name='Investment', related_name='sips', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, null=False)
    frequency = models.CharField(
        max_length=36,
        choices=SIPFrequency.choices(),  # Choices is a list of Tuple
        default=SIPFrequency.MONTHLY
    )
    last_transaction_date = models.DateField(auto_now=False, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

