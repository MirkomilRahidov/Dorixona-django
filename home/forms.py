from django import forms
from .model import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'brand', 'price', 'expiration_date', 'dosage', 'quantity', 'usage_instructions', 'side_effects', 'storage_conditions', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dori nomi'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brend nomi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Narxi (so‘m)'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dozasi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Miqdor'}),
            'usage_instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Qo‘llanilishi', 'rows': 3}),
            'side_effects': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nojo‘ya ta’sirlar', 'rows': 2}),
            'storage_conditions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saqlash sharoiti'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
