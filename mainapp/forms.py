import datetime
from django import forms
import requests

from mainapp import models as mainapp_models
from authapp import models as authapp_models


class CreateWorkForm(forms.ModelForm):
    class Meta:
        model = mainapp_models.Work
        exclude = ["user", "created_at", "is_deleted"]

    def clean_address(self):
        pk_entered_address = self.cleaned_data["address"]
        last_work_with_this_address = mainapp_models.Work.objects.filter(
            address=pk_entered_address
        )
        last_work = last_work_with_this_address.last()
        if last_work is not None:
            date_last_work = last_work.created_at.toordinal()
            now_date = datetime.datetime.now().toordinal()
            deltaTime = now_date - date_last_work
            if deltaTime < 14:
                raise forms.ValidationError("Эээээ.... 14 дней не прошло")
        return self.cleaned_data["address"]


class SupportForm(forms.Form):
    id_from = forms.IntegerField(widget=forms.HiddenInput)
    topic = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["id_from"].initial = user.pk

    def send_message(self):
        self.send_message_to_mail()
        print("Привет")

    def send_message_to_mobile(self):
        msg = f'От кого: {self.cleaned_data["id_from"]}. Сообщение: {self.cleaned_data["message"]}'
        sms_api = f"https://sms.ru/sms/send?api_id=9501034C-74AE-EEFB-1C8B-E2998518C53E&to=79236508766,79132106042,79132408203,79132172595,79612404234&msg={msg}&json=1"
        res = requests.get(sms_api)

    def send_message_to_mail(self):
        pass
