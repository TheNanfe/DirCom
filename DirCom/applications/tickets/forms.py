from django import forms
from django import forms
from .models import Comment, Ticket
from applications.users.models import User
from .ticket_utils import parse_json_data


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["email", "title", "content", "file", "category"]

    def __init__(self, *args, **kwargs):
        super(AddTicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AdminEditTicketForm(forms.ModelForm):
    field_order = ["agent", "category", "status", "urgency"]

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ('rejection_message', 'sub_category')

        widgets = {
            "user": forms.Select(
                attrs={"readonly": True}
            ),
            "content": forms.Textarea(
                attrs={"readonly": True}
            ),
            "email": forms.EmailInput(
                attrs={"readonly": True}
            ),
            "title": forms.TextInput(
                attrs={"readonly": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AdminEditTicketForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = User.objects.filter(role=2)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class RejectionMessageForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["rejection_message"]

    def __init__(self, *args, **kwargs):
        super(RejectionMessageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class EditTicketForm(forms.ModelForm):
    field_order = ["status", "content", "email"]

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ["agent", "rejection_message", "sub_category"]
        widgets = {
            "user": forms.Select(
                attrs={"readonly": True}
            ),
            "content": forms.Textarea(
                attrs={"readonly": True}
            ),
            "email": forms.EmailInput(
                attrs={"readonly": True}
            ),
            "title": forms.TextInput(
                attrs={"readonly": True}
            ),
            "urgency": forms.Select(
                attrs={"readonly": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EditTicketForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "file"]
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Escribe un comentario acerca de tu ticket..."}
            ),
        }
        labels = {"content": "Comentario"}

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
