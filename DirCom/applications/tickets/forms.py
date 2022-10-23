from django import forms
from django import forms
from .models import Comment, Ticket


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["email", "title", "content", "file", "category"]

    def __init__(self, *args, **kwargs):
        super(AddTicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "file"]
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escribe un comentario acerca de tu ticket...'}),
        }
        labels = {
            'content': 'Comentario'
        }

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
