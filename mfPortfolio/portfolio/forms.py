from django import  forms

from .models import MutualFund, MutualFundSIP

class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        exclude = ["last_transaction_date"]

class MutualFundSIPForm(forms.ModelForm):
    class Meta:
        model = MutualFundSIP
        exclude = ["last_transaction_date"]

