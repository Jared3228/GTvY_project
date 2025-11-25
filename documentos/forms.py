from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    """
    Formulario que usan los usuarios para subir/editar su documento.
    """
    class Meta:
        model = Documento
        # 👇 Usa 'nombre' en vez de 'titulo'
        fields = ['nombre', 'descripcion', 'archivo', 'marcado_para_revision']


class DocumentoRevisionForm(forms.ModelForm):
    """
    Formulario que usa el jefe para aprobar/rechazar.
    """
    class Meta:
        model = Documento
        fields = ['estado', 'marcado_para_revision']

    def clean_estado(self):
        estado = self.cleaned_data['estado']
        if estado not in ['aprobado', 'rechazado', 'revision']:
            raise forms.ValidationError(
                "Solo se puede establecer el estado a En revisión, Aprobado o Rechazado desde este formulario."
            )
        return estado
