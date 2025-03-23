from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price', 'city', 'property_type', 'listing_type')
    list_filter = ('property_type', 'listing_type', 'city')
    search_fields = ('title', 'description', 'address')

# Register your models
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
