from django import forms
from .models import PreTicket


class PreTicketForm(forms.Form):
    class Meta:
        model = PreTicket
        fields = ["fist_name", "last_name", "mail", "status", "subject", "form_type", "text_content"]


class FileHandlerForm(forms.Form):
    file = forms.FileField


class UploadFileHandlerForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    mail = forms.EmailField
    subject = forms.CharField(max_length=150)
    form_type = forms.CharField(max_length=50)
    text_content = forms.Textarea
