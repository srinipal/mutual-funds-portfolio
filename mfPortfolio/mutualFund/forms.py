from django import forms

from mutualFund.models import MutualFund


class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        fields = "__all__"

