from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import validate_email, EmailValidator, RegexValidator
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
            user.email = email
            user.has_completed_profile = False
            user.is_active = True
            if commit:
                user.save()
            users.append(user)
        return users


class ProfileCreateForm(forms.ModelForm):
    username_validator = RegexValidator(r'^[a-zA-Z]*$', message='Kan kun inneholde bokstavene a-z')
    new_username = forms.CharField(validators=[username_validator], label='Brukernavn', required=True, max_length=255,
                               help_text='Bruk helst NTNU-brukernavnet. Kan kun inneholde a-z. Ikke bruk noe "tull".')

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].required = True

    def save(self, commit=True):
        self.instance.username = self.cleaned_data['new_username']
        self.instance.has_completed_profile = True
        super(ProfileCreateForm, self).save(commit)

    class Meta:
        model = Member
        fields = ['new_username', 'first_name', 'last_name', 'phone']


class GClefForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GClefForm, self).__init__(*args, **kwargs)
        for m in Member.get_potential_pangs():
            field = forms.BooleanField(initial=False, label=m.__str__(), required=False)
            field.member = m
            self.fields['member_{}'.format(m.pk)] = field

    def get_new_pangs(self):
        for name, value in self.cleaned_data.items():
            if value:
                yield self.fields[name].member
