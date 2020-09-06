from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

from .models import MutualFund, MutualFundSIP, SIPRebalance
from .utils import process_utils
from mutualFund.models import MutualFund as MutualFundGlobal

class DateInput(forms.DateInput):
    input_type = 'date'


class MutualFundForm(forms.ModelForm):
    class Meta:
        model = MutualFund
        exclude = ["last_transaction_date", "active", "created_by"]

    def __init__(self, *args, **kwargs):
        super(MutualFundForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial_dict = kwargs.get('initial')
            if 'fields_to_disable' in initial_dict:
                fields_to_disable = initial_dict['fields_to_disable']
                for field_to_disable in fields_to_disable:
                    self.fields[field_to_disable].disabled = True

    def save(self, *args, **kwargs):
        # Set the user
        user = kwargs.pop('user', None)
        if not self.instance.pk:
            self.instance.created_by = user
        super(MutualFundForm, self).save(*args, **kwargs)


class MutualFundSIPForm(forms.ModelForm):
    class Meta:
        model = MutualFundSIP
        exclude = ["last_transaction_date", "created_by"]
        widgets = {
            'start_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MutualFundSIPForm, self).__init__(*args, **kwargs)
        self.fields['mutual_fund'].queryset = MutualFund.objects.filter(active=True, created_by=user)

        if 'initial' in kwargs:
            initial_dict = kwargs.get('initial')
            if 'fields_to_disable' in initial_dict:
                fields_to_disable = initial_dict['fields_to_disable']
                for field_to_disable in fields_to_disable:
                    self.fields[field_to_disable].disabled = True

    @staticmethod
    def drop_sip_event(sip_id):
        event_drop_sql = process_utils.build_sip_delete_event(sip_id)
        with connection.cursor() as cursor:
            cursor.execute(event_drop_sql)
            cursor.close()

    @staticmethod
    def create_sip_event(sip_id, start_date, frequency):
        event_create_sql = process_utils.build_sip_create_event(sip_id, start_date, frequency)
        print(event_create_sql)
        with connection.cursor() as cursor:
            cursor.execute(event_create_sql)
            cursor.close()

    @staticmethod
    def event_scheduling_with_db(sip_instance, cleanup_old_event=None, create_event=False):
        sip_id = sip_instance.pk
        start_date = sip_instance.start_date
        frequency = sip_instance.frequency

        if cleanup_old_event:
            MutualFundSIPForm.drop_sip_event(sip_id)
        if create_event:
            MutualFundSIPForm.create_sip_event(sip_id, start_date, frequency)

    def save(self, *args, **kwargs):
        sip_instance = self.instance
        cleanup_old_event = sip_instance.pk

        # Set the user
        user = kwargs.pop('user', None)
        if not cleanup_old_event:
            self.instance.created_by = user
        super(MutualFundSIPForm, self).save(*args, **kwargs)

        if self.has_changed():
            MutualFundSIPForm.event_scheduling_with_db(sip_instance, cleanup_old_event, sip_instance.active)


class SIPRebalanceForm(forms.ModelForm):
    class Meta:
        model = SIPRebalance
        exclude = ["created_by", "re_balance"]

