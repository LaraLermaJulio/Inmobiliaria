from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price', 'discount_percentage', 'discounted_price', 'city', 'property_type', 'listing_type')
    list_filter = ('property_type', 'listing_type', 'city')
    search_fields = ('title', 'description', 'address')
    
    def discounted_price(self, obj):
        """Display the discounted price in the admin list"""
        if obj.discount_percentage > 0:
            discount_amount = (obj.price * obj.discount_percentage) / 100
            return obj.price - discount_amount
        return obj.price
    
    discounted_price.short_description = 'Precio con descuento'

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
