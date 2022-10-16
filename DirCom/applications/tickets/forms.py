from django import forms
from django import forms
from .models import Ticket

class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super(AddTicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'