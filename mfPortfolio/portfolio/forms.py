from django import forms

from .models import MutualFund, MutualFundSIP

class DateInput(forms.DateInput):
    input_type = 'date'

class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        exclude = ["last_transaction_date"]

class MutualFundSIPForm(forms.ModelForm):
    class Meta:
        model = MutualFundSIP
        exclude = ["last_transaction_date"]
        widgets = {
            'start_date': DateInput()
        }
