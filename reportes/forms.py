# reportes/forms.py
from django import forms

class ConstanciaResidenciasForm(forms.Form):
    nombre = forms.CharField(max_length=150, label='Nombre del alumno')
    numero_control = forms.CharField(max_length=20, label='Número de control')
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
