from django import forms

class DatosBasicosReporteForm(forms.Form):
    nombre_alumno = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numero_control = forms.CharField(
        label='Número de control',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha = forms.DateField(
        label='Fecha de emisión',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
