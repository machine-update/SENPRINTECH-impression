from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Prenom", max_length=150, required=False)
    last_name = forms.CharField(label="Nom", max_length=150, required=False)
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "ex: senprintech",
            "first_name": "Votre prenom",
            "last_name": "Votre nom",
            "email": "votre@email.com",
            "password1": "Mot de passe",
            "password2": "Confirmer le mot de passe",
        }
        labels = {
            "username": "Nom d'utilisateur",
            "password1": "Mot de passe",
            "password2": "Confirmation",
        }
        for name, field in self.fields.items():
            field.label = labels.get(name, field.label)
            field.help_text = ""
            field.widget.attrs.update(
                {
                    "class": "auth-input",
                    "placeholder": placeholders.get(name, ""),
                }
            )


class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "auth-input", "placeholder": "Votre nom d'utilisateur"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "auth-input", "placeholder": "Votre mot de passe"}
        )
