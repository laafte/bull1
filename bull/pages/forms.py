from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Hidden
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Brukernavn'
        self.fields['password'].label = 'Passord'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'django.contrib.auth.views.login'
        self.helper.layout = Layout(
            Field('username', placeholder='Brukernavn', ),
            Field('password', placeholder='Passord'),
            Submit('submit', 'Logg inn'),
            Hidden('next', '{{ next }}'),
        )
