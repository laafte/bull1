from django.contrib.auth.forms import AuthenticationForm
from django import forms


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Brukernavn", widget=forms.TextInput(attrs={'placeholder': 'Brukernavn',
                                                                                 'class': 'span2'}))
    password = forms.CharField(label="Passord", widget=forms.PasswordInput(attrs={'placeholder': 'Passord',
                                                                                  'class': 'span2'}))


def include_login_form(request):
    form = MyAuthenticationForm()
    return {'login_form': form}
