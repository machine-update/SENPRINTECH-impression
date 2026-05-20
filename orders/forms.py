from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "city",
            "delivery_method",
            "notes",
        ]
        labels = {
            "full_name": "Nom complet",
            "phone": "Téléphone",
            "email": "Email",
            "address": "Adresse",
            "city": "Ville",
            "delivery_method": "Mode de livraison",
            "notes": "Notes commande",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Votre nom complet"}),
            "phone": forms.TextInput(attrs={"placeholder": "+221 ..."}),
            "email": forms.EmailInput(attrs={"placeholder": "votre@email.com"}),
            "address": forms.TextInput(attrs={"placeholder": "Adresse de retrait/livraison"}),
            "city": forms.TextInput(attrs={"placeholder": "Dakar, Thies..."}),
            "notes": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Delai souhaite, details livraison, precision sur les fichiers...",
            }),
        }
