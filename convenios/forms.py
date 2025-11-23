from django import forms
from .models import Convenio

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ['nombre', 'fecha_convenio', 'fecha_expiracion', 'contacto', 'descripcion']
        widgets = {
            'fecha_convenio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_expiracion': forms.DateInput(attrs={'type': 'date'}),
        }
