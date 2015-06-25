from django import forms
from django.core.validators import validate_email, EmailValidator
from members.models import Member


class BulkAddForm(forms.Form):
    """
    A form used to add many users from their e-mail addresses
    """
    emails = forms.CharField(
        label="E-postadresser",
        widget=forms.Textarea,
        help_text="Skriv inn e-postadresser, separert med semikolon",
    )

    def clean_emails(self):
        emails = self.cleaned_data.get('emails')
        mail_list = emails.strip(";").split(";")
        for email in mail_list:
            EmailValidator(message="Én eller flere av adressene er ugyldige")(email)
        return mail_list

    def save(self, commit=True):
        """
        Creates new Member-objects and saves them
        """
        users = []
        emails = self.cleaned_data["emails"]
        for email in emails:
            user = Member.objects.create_user(email)
            if commit:
                user.save()
            users.append(user)
        return users