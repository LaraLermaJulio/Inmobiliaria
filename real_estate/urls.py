from django.urls import path
from . import views
from .views import estadisticas_pdf

urlpatterns = [
    # Existing URLs
    path('', views.index, name='index'),
    path('ventas/', views.ventas, name='ventas'),
    path('renta/', views.renta, name='renta'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('detalle-propiedad/<int:property_id>/', views.property_detail, name='detalle_propiedad'),
    path('estadisticas/', views.estadisticas_vistas, name='estadisticas_vistas'),
    # New URLs for property management
    path('mis-propiedades/', views.my_properties, name='my_properties'),
    path('agregar-propiedad/', views.add_property, name='add_property'),
    path('editar-propiedad/<int:id>/', views.edit_property, name='edit_property'),
    path('eliminar-propiedad/<int:id>/', views.delete_property, name='delete_property'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('search/', views.search_properties, name='search_properties'),
    path('api/search', views.api_search, name='api_search'),
    # Add this to your urlpatterns list
    path('api/discounted-properties/', views.discounted_properties, name='discounted_properties'),
    path('property/<int:property_id>/contact/', views.property_contact, name='property_contact'),
    path('my-property-contacts/', views.property_contacts, name='property_contacts'),
    path('detalle-propiedad/<int:property_id>/pdf/', views.generate_property_pdf, name='property_pdf'),
    path('estadisticas/pdf/', estadisticas_pdf, name='estadisticas_pdf'),
    path('toggle-property-visibility/', views.toggle_property_visibility, name='toggle_property_visibility'),
    
]