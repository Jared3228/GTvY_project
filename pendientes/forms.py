# pendientes/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .models import Pendiente

User = get_user_model()


class PendienteForm(forms.ModelForm):
    # Sobreescribimos asignado_a para que NO sea obligatorio
    asignado_a = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Asignar a usuario',
        help_text='Opcional: selecciona un usuario específico.'
    )

    # Nuevo campo: grupo/rol
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Asignar a rol',
        help_text='Opcional: si seleccionas un rol, se creará un pendiente para cada usuario de ese rol.'
    )

    class Meta:
        model = Pendiente
        fields = ['titulo', 'descripcion', 'asignado_a', 'grupo', 'fecha_limite']
        widgets = {
            # 👇 Esto hace que salga un calendario en HTML5
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        asignado_a = cleaned.get('asignado_a')
        grupo = cleaned.get('grupo')

        # Debe haber al menos uno de los dos
        if not asignado_a and not grupo:
            raise forms.ValidationError(
                'Debes seleccionar un usuario o un rol para asignar el pendiente.'
            )

        return cleaned
