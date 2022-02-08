from pyexpat import model
from django import forms

from .models import User


class UserCreateForm(forms.ModelForm):

    password1 = forms.CharField(
        label=("Contraseña"),
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Contraseña'
                   }
        )
    )

    password2 = forms.CharField(
        label=("Contraseña"),
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Repetir Contraseña'
                   }
        )
    )

    class Meta:

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )
