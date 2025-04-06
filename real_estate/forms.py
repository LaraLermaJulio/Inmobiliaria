# Asumiendo que tienes un archivo forms.py con un PropertyForm
# Si no existe, deberás crearlo con este contenido

from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'discount_percentage', 'address', 
            'city', 'state', 'bedrooms', 'bathrooms', 'area', 
            'parking_spaces', 'property_type', 'listing_type', 
            'is_featured', 'accepts_pets', 'is_furnished', 'has_security',
            'latitude', 'longitude'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'discount_percentage': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']
