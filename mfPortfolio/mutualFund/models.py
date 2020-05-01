from django.db import models
from .utils.common_enums import AssetClass
# Create your models here.


class MutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    mf_name = models.CharField(max_length=256)
    holdings_url = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_scrape_date = models.DateField(null=True)

    def __str__(self):
        return self.mf_name


class MutualFundAssetAllocation(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund = models.ForeignKey(MutualFund, related_name='assetAllocation', on_delete=models.CASCADE)
    asset_class = models.CharField(
        max_length=36,
        choices=AssetClass.choices()
    )
    percentage = models.DecimalField(decimal_places=2, max_digits=22, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class MutualFundScrapeLog(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund = models.ForeignKey(MutualFund, related_name='scrapeLog', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class MutualFundEquityAllocation(models.Model):
    id = models.AutoField(primary_key=True)
    mutual_fund = models.ForeignKey(MutualFund, related_name='equityAllocation', on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=256)
    sector = models.CharField(max_length=256)
    sector_total = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    holdings_value = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    holdings_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    prev_month_change_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    past_year_highest_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    past_year_lowest_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    one_year_highest_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    one_year_lowest_percent = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    prev_month_change_qty = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    category = models.CharField(max_length=32)
    group_name = models.DecimalField(decimal_places=2, max_digits=22, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

