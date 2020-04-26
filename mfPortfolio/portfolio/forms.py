from django import forms

from .models import MutualFund, MutualFundSIP

class DateInput(forms.DateInput):
    input_type = 'date'

class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        exclude = ["last_transaction_date", "active"]

class MutualFundSIPForm(forms.ModelForm):
    class Meta:
        model = MutualFundSIP
        exclude = ["last_transaction_date"]
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(MutualFundSIPForm, self).__init__(*args, **kwargs)
        if ('initial' in kwargs):
            initial_dict = kwargs.get('initial')
            if ('fields_to_disable' in initial_dict):
                fields_to_disable = initial_dict['fields_to_disable']
                for field_to_disable in fields_to_disable:
                    self.fields[field_to_disable].disabled = True
