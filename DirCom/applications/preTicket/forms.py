from django import forms
from .models import PreTicket


class PreTicketForm(forms.Form):
    class Meta:
        model = PreTicket
        fields = ["fist_name", "last_name", "mail", "status", "subject", "form_type", "text_content"]
