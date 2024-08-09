from django import forms
from .models import Activity
import datetime

class ActivityForm(forms.ModelForm):
    rustperiode = forms.BooleanField(required=False, label='Rustdagen aanvullen tot gisteren', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Activity
        fields = ['date', 'musclegroup', 'cardioexercise', 'duration', 'location', 'notes', 'is_rest', 'rustperiode']
        labels = {
            'date': 'Datum',
            'musclegroup': 'Spiergroep',
            'cardioexercise': 'Cardio-oefening',
            'duration': 'Duur (minuten)',
            'location': 'Locatie',            
            'notes': 'Notitie',
            'is_rest': 'Rustdag',
        }        
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'musclegroup': forms.Select(attrs={'class': 'form-control'}),
            'cardioexercise': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),
            'location': forms.Select(attrs={'class': 'form-control'}),            
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_rest': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.date.today()
        self.fields['location'].initial = 1
