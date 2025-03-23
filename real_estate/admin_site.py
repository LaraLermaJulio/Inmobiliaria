from django.contrib.admin import AdminSite
from .models import Property
from .admin import PropertyAdmin

class UserAdminSite(AdminSite):
    site_header = 'Inmobiliaria - Panel de Usuario'
    site_title = 'Panel de Usuario'
    index_title = 'Administración de Propiedades'

# Create custom admin site
user_admin_site = UserAdminSite(name='user_admin')

# Register models with the custom admin site
user_admin_site.register(Property, PropertyAdmin)