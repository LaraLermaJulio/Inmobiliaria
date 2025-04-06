from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    # Add the owner field
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    
    PROPERTY_TYPE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('terreno', 'Terreno'),
        ('comercial', 'Local Comercial'),
        ('oficina', 'Oficina'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('venta', 'Venta'),
        ('renta', 'Renta'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Descuento (%)")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Estado")
    bedrooms = models.PositiveSmallIntegerField(default=0, verbose_name="Habitaciones")
    bathrooms = models.PositiveSmallIntegerField(default=0, verbose_name="Baños")
    area = models.PositiveIntegerField(help_text="Área en metros cuadrados", verbose_name="Superficie")
    parking_spaces = models.PositiveSmallIntegerField(default=0, verbose_name="Estacionamientos")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, verbose_name="Tipo de Propiedad")
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, verbose_name="Tipo de Listado")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    accepts_pets = models.BooleanField(default=False, verbose_name="Acepta Mascotas")
    is_furnished = models.BooleanField(default=False, verbose_name="Amueblado")
    has_security = models.BooleanField(default=False, verbose_name="Seguridad 24h")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    # Map coordinates
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True, verbose_name="Latitud")
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True, verbose_name="Longitud")
    
    def __str__(self):
        return self.title
    
    def get_discounted_price(self):
        """Calcula el precio con descuento aplicado"""
        if self.discount_percentage > 0:
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price
    
    def has_discount(self):
        """Verifica si la propiedad tiene un descuento aplicado"""
        return self.discount_percentage > 0
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE, verbose_name="Propiedad")
    image = models.ImageField(upload_to='properties/', verbose_name="Imagen")
    is_main = models.BooleanField(default=False, verbose_name="Imagen Principal")
    
    def __str__(self):
        return f"Imagen para {self.property.title}"
    
    class Meta:
        verbose_name = "Imagen de Propiedad"
        verbose_name_plural = "Imágenes de Propiedades"

class PropertyCall(models.Model):
    CALL_STATUS_CHOICES = [
        ('completed', 'Completada'),
        ('missed', 'Perdida'),
        ('busy', 'Ocupado'),
        ('failed', 'Fallida'),
        ('in-progress', 'En Progreso'),
    ]
    
    CALL_TYPE_CHOICES = [
        ('inbound', 'Entrante'),
        ('outbound', 'Saliente'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='calls')
    caller_name = models.CharField(max_length=100, blank=True, null=True)
    caller_number = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, default='completed')
    call_type = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES, default='inbound')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Call from {self.caller_number} about {self.property.title}"
