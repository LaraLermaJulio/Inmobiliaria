from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Existing URLs
    path('', views.index, name='index'),
    path('ventas/', views.ventas, name='ventas'),
    path('renta/', views.renta, name='renta'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('detalle-propiedad/<int:id>/', views.detalle_propiedad, name='detalle_propiedad'),
    
    # New URLs for property management
    path('mis-propiedades/', views.my_properties, name='my_properties'),
    path('agregar-propiedad/', views.add_property, name='add_property'),
    path('editar-propiedad/<int:id>/', views.edit_property, name='edit_property'),
    path('eliminar-propiedad/<int:id>/', views.delete_property, name='delete_property'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]