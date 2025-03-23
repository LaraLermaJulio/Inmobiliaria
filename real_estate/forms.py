from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'area', 'bedrooms', 'bathrooms', 
                  'parking_spaces', 'property_type', 'listing_type', 'city', 'state', 
                  'address', 'latitude', 'longitude', 'is_furnished', 'accepts_pets', 'has_security']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Ej. 19.4326'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Ej. -99.1332'}),
        }

class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(label='Imagen', required=False)
    delete = forms.BooleanField(required=False, initial=False, label='Eliminar')
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']
