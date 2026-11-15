from django import forms
from django.utils import timezone

from .models import Encargos


class EncargoForm(forms.ModelForm):
    fecharetiro = forms.DateField(
        label='Fecha de retiro', input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'placeholder': 'Dia/Mes/Año', 'maxlength': '10', 'inputmode': 'numeric',
        }),
        error_messages={'invalid': 'Ingresa una fecha válida por ejemplo: 22/11/2026.'},
    )
    unidadesApedir = forms.IntegerField(
        label='Cantidad de unidades', min_value=1, max_value=3,
        error_messages={
            'invalid': 'Ingresa una cantidad válida entre 1 y 3 unidades.',
            'min_value': 'La cantidad debe estar entre 1 y 3 unidades.',
            'max_value': 'La cantidad debe estar entre 1 y 3 unidades.',
        },
    )

    class Meta:
        model = Encargos
        fields = ['nombre', 'correo', 'fecharetiro', 'unidadesApedir']
        labels = {'nombre': 'Nombre', 'correo': 'Correo electrónico',
                  'fecharetiro': 'Fecha de retiro'}
        error_messages = {
            'correo': {'invalid': 'Ingresa un correo electrónico válido.'},
        }
    def clean_fecharetiro(self):
        fecha = self.cleaned_data['fecharetiro']
        if fecha < timezone.localdate():
            raise forms.ValidationError('La fecha de retiro no puede ser anterior al día de hoy.')
        return fecha
