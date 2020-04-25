from django import  forms
from urllib3 import fields

from .models import MutualFund

class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        fields = "__all__"