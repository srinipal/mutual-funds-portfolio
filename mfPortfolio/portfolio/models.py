from django.contrib.auth.models import User
from django.db import models

from mutualFund.models import MutualFund as MutualFundGlobal
from .utils.common_enums import SIPFrequency


class MutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund_global = models.ForeignKey(MutualFundGlobal, verbose_name='Mutual Fund', related_name='investments', on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    last_transaction_date = models.DateField(auto_now=False, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.mutual_fund_global.mf_name

    def active_sips(self):
        return self.sips.filter(active=True)


class MutualFundSIP(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    mutual_fund = models.ForeignKey(MutualFund, verbose_name='Add to Investment', related_name='sips', on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, null=False)
    frequency = models.CharField(
        max_length=36,
        choices=SIPFrequency.choices(),  # Choices is a list of Tuple
        default=SIPFrequency.MONTHLY
    )
    last_transaction_date = models.DateField(auto_now=False, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class PortfolioRebalance(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SIPRebalance(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund_global = models.ForeignKey(MutualFundGlobal, verbose_name='Mutual Fund', on_delete=models.DO_NOTHING)
    re_balance = models.ForeignKey(PortfolioRebalance, verbose_name='sips', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

