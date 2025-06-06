from django.shortcuts import render, get_object_or_404
from .models import Property, PropertyImage
from django.db.models import Q, Count, Sum  # Add Sum here
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageForm
from django.forms import modelformset_factory
# Add these imports at the top of the file
from django.http import JsonResponse
from .models import Property
from django.urls import reverse
from .models import PropertyContact
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import HttpResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.units import inch
import json
import io

def index(request):
    featured_properties = Property.objects.filter(is_featured=True)[:5]
    
    # Add main image to each property
    for prop in featured_properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    return render(request, 'real_estate/index.html', {
        'featured_properties': featured_properties
    })

def ventas(request):
    search_query = request.GET.get('search', '')
    properties = Property.objects.filter(listing_type='venta', is_visible=True)
    
    # Get unique cities for the location filter
    cities = Property.objects.filter(listing_type='venta').values_list('city', flat=True).distinct()
    
    # Apply filters if they exist in the request
    location = request.GET.get('location')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    bedrooms = request.GET.getlist('bedrooms')
    bathrooms = request.GET.getlist('bathrooms')
    property_type = request.GET.get('property_type')
    area_min = request.GET.get('area_min')
    area_max = request.GET.get('area_max')
    
    # Apply search query filter
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Apply location filter
    if location:
        properties = properties.filter(city=location)
    
    # Apply price filters
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)
    
    # Apply bedroom filters (if any are selected)
    if bedrooms:
        # Handle the 4+ case specially
        if '4' in bedrooms:
            bedroom_filters = [int(b) for b in bedrooms if b != '4']
            properties = properties.filter(
                Q(bedrooms__in=bedroom_filters) | Q(bedrooms__gte=4)
            )
        else:
            properties = properties.filter(bedrooms__in=[int(b) for b in bedrooms])
    
    # Apply bathroom filters (if any are selected)
    if bathrooms:
        # Handle the 3+ case specially
        if '3' in bathrooms:
            bathroom_filters = [int(b) for b in bathrooms if b != '3']
            properties = properties.filter(
                Q(bathrooms__in=bathroom_filters) | Q(bathrooms__gte=3)
            )
        else:
            properties = properties.filter(bathrooms__in=[int(b) for b in bathrooms])
    
    # Apply property type filter
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    # Apply area filters
    if area_min:
        properties = properties.filter(area__gte=area_min)
    if area_max:
        properties = properties.filter(area__lte=area_max)
    
    # Add main image to each property
    for prop in properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    # Prepare filter values to pass back to template
    filters = {
        'location': location or '',
        'price_min': price_min or '',
        'price_max': price_max or '',
        'bedrooms': bedrooms or [],
        'bathrooms': bathrooms or [],
        'property_type': property_type or '',
        'area_min': area_min or '',
        'area_max': area_max or '',
    }
    
    context = {
        'properties': properties,
        'search_query': search_query,
        'cities': cities,
        'filters': filters
    }
    return render(request, 'real_estate/ventas.html', context)

def renta(request):
    search_query = request.GET.get('search', '')
    properties = Property.objects.filter(listing_type='renta', is_visible=True)
    
    # Get unique cities for the location filter
    cities = Property.objects.filter(listing_type='renta').values_list('city', flat=True).distinct()
    
    # Apply filters if they exist in the request
    location = request.GET.get('location')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    bedrooms = request.GET.getlist('bedrooms')
    bathrooms = request.GET.getlist('bathrooms')
    property_type = request.GET.get('property_type')
    area_min = request.GET.get('area_min')
    area_max = request.GET.get('area_max')
    
    # Apply search query filter
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query)
        )
    
    # Apply location filter
    if location:
        properties = properties.filter(city=location)
    
    # Apply price filters
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)
    
    # Apply bedroom filters (if any are selected)
    if bedrooms:
        # Handle the 4+ case specially
        if '4' in bedrooms:
            bedroom_filters = [int(b) for b in bedrooms if b != '4']
            properties = properties.filter(
                Q(bedrooms__in=bedroom_filters) | Q(bedrooms__gte=4)
            )
        else:
            properties = properties.filter(bedrooms__in=[int(b) for b in bedrooms])
    
    # Apply bathroom filters (if any are selected)
    if bathrooms:
        # Handle the 3+ case specially
        if '3' in bathrooms:
            bathroom_filters = [int(b) for b in bathrooms if b != '3']
            properties = properties.filter(
                Q(bathrooms__in=bathroom_filters) | Q(bathrooms__gte=3)
            )
        else:
            properties = properties.filter(bathrooms__in=[int(b) for b in bathrooms])
    
    # Apply property type filter
    if property_type:
        properties = properties.filter(property_type=property_type)
    
    # Apply area filters
    if area_min:
        properties = properties.filter(area__gte=area_min)
    if area_max:
        properties = properties.filter(area__lte=area_max)
    
    # Add main image to each property
    for prop in properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    # Prepare filter values to pass back to template
    filters = {
        'location': location or '',
        'price_min': price_min or '',
        'price_max': price_max or '',
        'bedrooms': bedrooms or [],
        'bathrooms': bathrooms or [],
        'property_type': property_type or '',
        'area_min': area_min or '',
        'area_max': area_max or '',
    }
    
    return render(request, 'real_estate/renta.html', {
        'properties': properties,
        'cities': cities,
        'filters': filters,
        'search_query': search_query
    })

def nosotros(request):
    return render(request, 'real_estate/nosotros.html')

def contacto(request):
    return render(request, 'real_estate/contacto.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect all users to index instead of admin
            return redirect('index')
        else:
            # Return an error message for invalid login
            return render(request, 'real_estate/login.html', {
                'form_errors': True,
                'error_message': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'real_estate/login.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect all users (including admins) to index page
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'real_estate/login.html', {'form': form})

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    # Incrementar el contador de vistas
    property.views += 1
    property.save()
    
    # Registrar la vista en el mes actual
    current_month = timezone.now().strftime('%Y-%m')
    
    # Aquí deberías tener un modelo para registrar vistas por mes
    # Por ejemplo: PropertyViewMonth
    # PropertyViewMonth.objects.create_or_update(
    #     property=property,
    #     month=current_month,
    #     views=F('views') + 1
    # )
    
    # Get property images using the same pattern as in ventas/renta views
    property_images = property.images.all()
    main_images = property.images.filter(is_main=True)
    if main_images.exists():
        main_image = main_images.first()
    else:
        main_image = property_images.first() if property_images.exists() else None
    
    # Get 3 random similar properties of the same listing type (rent or sale)
    similar_properties = Property.objects.filter(
        listing_type=property.listing_type
    ).exclude(
        id=property.id
    ).order_by('?')[:3]  # The '?' orders randomly
    
    # Add main image to each similar property
    for prop in similar_properties:
        similar_main_images = prop.images.filter(is_main=True)
        if similar_main_images.exists():
            prop.main_image = similar_main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    context = {
        'property': property,
        'property_images': property_images,
        'main_image': main_image,
        'similar_properties': similar_properties,
    }
    
    return render(request, 'real_estate/detalle_propiedad.html', context)

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    
    # Add main image to each property
    for prop in properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    return render(request, 'real_estate/my_properties.html', {
        'properties': properties
    })

@login_required
def add_property(request):
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=3)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())
        
        if form.is_valid() and formset.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            
            # Process images
            instances = []
            for image_form in formset.cleaned_data:
                # Only process if there's an image
                if image_form and 'image' in image_form and image_form['image']:
                    photo = PropertyImage(
                        property=property,
                        image=image_form['image'],
                        is_main=False  # Set all to false initially
                    )
                    photo.save()
                    instances.append(photo)
            
            # Handle main image selection
            main_image_index = request.POST.get('main_image')
            if main_image_index is not None and main_image_index.isdigit() and instances:
                main_image_index = int(main_image_index)
                if main_image_index < len(instances):
                    instances[main_image_index].is_main = True
                    instances[main_image_index].save()
            
            return redirect('my_properties')
    else:
        form = PropertyForm()
        formset = ImageFormSet(queryset=PropertyImage.objects.none())
    
    return render(request, 'real_estate/property_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Agregar Propiedad'
    })

@login_required
def edit_property(request, id):
    property = get_object_or_404(Property, id=id, owner=request.user)
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=1)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        formset = ImageFormSet(request.POST, request.FILES, queryset=property.images.all())
        
        if form.is_valid() and formset.is_valid():
            property = form.save()
            
            # Process the formset
            instances = formset.save(commit=False)
            
            # Save new or modified instances
            for instance in instances:
                # Only save if there's an actual image
                if instance.image:
                    instance.property = property
                    instance.save()
            
            # Handle main image selection
            if 'main_image' in request.POST:
                main_image_id = request.POST.get('main_image')
                # Debug print to check the value
                print(f"Main image ID: {main_image_id}")
                
                # First, set all images for this property to not be the main image
                PropertyImage.objects.filter(property=property).update(is_main=False)
                
                # Then, set the selected image as the main image
                try:
                    main_image = PropertyImage.objects.get(id=main_image_id, property=property)
                    main_image.is_main = True
                    main_image.save()
                    print(f"Set image {main_image_id} as main")
                except PropertyImage.DoesNotExist:
                    print(f"Image with ID {main_image_id} not found")
            
            return redirect('my_properties')
        else:
            # Add this to debug form errors
            print(f"Form errors: {form.errors}")
            print(f"Formset errors: {formset.errors}")
    else:
        form = PropertyForm(instance=property)
        formset = ImageFormSet(queryset=property.images.all())
    
    return render(request, 'real_estate/property_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Editar Propiedad',
        'property': property
    })

@login_required
def delete_property(request, id):
    property = get_object_or_404(Property, id=id, owner=request.user)
    
    if request.method == 'POST':
        property.delete()
        return redirect('my_properties')
    
    return render(request, 'real_estate/delete_property.html', {
        'property': property
    })


@login_required
def delete_image(request, image_id):
    # Get the image
    image = get_object_or_404(PropertyImage, id=image_id)
    
    # Check if the user owns the property
    if image.property.owner != request.user:
        return redirect('my_properties')
    
    # Store the property id for redirection
    property_id = image.property.id
    
    # Delete the image
    image.delete()
    
    # Redirect back to the property edit page
    return redirect('edit_property', id=property_id)


def search_properties(request):
    query = request.GET.get('q', '').strip()  # Elimina espacios en blanco
    
    if not query:
        return render(request, 'real_estate/search_results.html', {
            'properties': Property.objects.none(),
            'query': query,
        })
    
    # Buscar propiedades en ventas
    ventas_properties = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query) |
        Q(state__icontains=query),
        listing_type='venta',
        is_visible=True  # Solo mostrar propiedades visibles
    )
    
    # Buscar propiedades en rentas
    rentas_properties = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query) |
        Q(state__icontains=query),
        listing_type='renta',
        is_visible=True  # Solo mostrar propiedades visibles
    )
    
    # Redirigir a la página correspondiente según los resultados
    if ventas_properties.exists():
        # Si hay resultados en ventas, redirigir a la página de ventas con el parámetro search
        return redirect(f'/ventas/?search={query}')
    elif rentas_properties.exists():
        # Si hay resultados en rentas, redirigir a la página de rentas con el parámetro search
        return redirect(f'/renta/?search={query}')
    else:
        # Si no hay resultados, mostrar la página de resultados vacíos
        return render(request, 'real_estate/search_results.html', {
            'properties': Property.objects.none(),
            'query': query,
            'no_results': True
        })


# Agregar esta vista
def api_search(request):
    query = request.GET.get('q', '')
    listing_type = request.GET.get('type', '')
    
    if query and listing_type:
        properties = Property.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        ).filter(listing_type=listing_type)
        
        return JsonResponse({'found': properties.exists()})
    
    return JsonResponse({'found': False})


# Add the discounted_properties function at the module level
def discounted_properties(request):
    """API endpoint to get properties with discounts"""
    properties = Property.objects.filter(discount_percentage__gt=0)
    
    properties_data = []
    for prop in properties:
        discounted_price = float(prop.price) - (float(prop.price) * float(prop.discount_percentage) / 100)
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'price': float(prop.price),
            'discount_percentage': float(prop.discount_percentage),
            'discounted_price': round(discounted_price, 2)
        })
    
    return JsonResponse({'properties': properties_data})


@login_required
def call_tracking_dashboard(request):
    """View to display a list of properties with call statistics"""
    # Get properties owned by the current user
    properties = Property.objects.filter(owner=request.user)
    
    # Get call statistics for each property
    property_stats = []
    for property in properties:
        # In a real implementation, you would have a PropertyCall model
        # For now, we'll create dummy data
        property_stats.append({
            'property': property,
            'total_calls': 0,
            'completed_calls': 0,
            'missed_calls': 0,
            'last_call': None
        })
    
    context = {
        'property_stats': property_stats
    }
    
    return render(request, 'real_estate/call_tracking_list.html', context)


def debug_search(request):
    """A temporary debug view to check if properties exist"""
    query = "Celaya"
    
    ventas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='venta'
    )
    
    rentas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='renta'
    )
    
    data = {
        'query': query,
        'ventas_count': ventas.count(),
        'rentas_count': rentas.count(),
        'ventas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in ventas],
        'rentas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in rentas],
    }
    
    return JsonResponse(data)


@require_POST
def property_contact(request, property_id):
    """Handle property contact form submissions"""
    try:
        property_obj = Property.objects.get(id=property_id)
        
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Create contact record
        contact = PropertyContact.objects.create(
            property=property_obj,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        return JsonResponse({'success': True, 'message': 'Mensaje enviado correctamente'})
    except Property.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Propiedad no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Añadir una vista para mostrar los contactos de las propiedades del usuario
@login_required
def property_contacts(request):
    """View to display contacts for properties owned by the current user"""
    # Get properties owned by the current user
    user_properties = Property.objects.filter(owner=request.user)
    
    # Get contacts for those properties
    contacts = PropertyContact.objects.filter(property__in=user_properties)
    
    context = {
        'contacts': contacts
    }
    
    return render(request, 'real_estate/property_contacts.html', context)


from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def estadisticas(request):
    """Vista para mostrar estadísticas de vistas de propiedades"""
    # Obtener propiedades del usuario actual
    properties = Property.objects.filter(owner=request.user)
    
    # Obtener las 5 propiedades más vistas
    top_properties = properties.order_by('-views')[:5]
    
    # Crear datos de vistas mensuales
    monthly_views_data = []
    
    # Obtener el mes actual
    current_month = timezone.now().strftime('%Y-%m')
    current_month_date = f"{current_month}-01"  # Formato YYYY-MM-DD para JavaScript
    
    # Sumar todas las vistas de las propiedades para el mes actual
    total_views = properties.aggregate(Sum('views'))['views__sum'] or 0
    
    # Agregar el mes actual con el total de vistas
    monthly_views_data.append({
        'month': current_month_date,
        'total_views': total_views
    })
    
    # Imprimir para depuración
    print("Datos mensuales enviados al frontend:", monthly_views_data)
    
    context = {
        'top_properties': top_properties,
        'monthly_views': json.dumps(monthly_views_data, cls=DjangoJSONEncoder)
    }
    
    return render(request, 'real_estate/estadisticas.html', context)


# Agregar esta nueva vista para generar el PDF
def estadisticas_pdf(request):
    # Crear un objeto de respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estadisticas_inmobiliaria.pdf"'
    
    # Crear el documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos para el documento
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título del documento
    elements.append(Paragraph("Relación de vistas de propiedades", title_style))
    elements.append(Spacer(1, 20))
    
    # Obtener los datos de propiedades (ajusta esto según tu modelo)
    from .models import Property
    
    # Datos para la tabla
    properties = Property.objects.all()
    data = [['Propiedad', 'Ubicación', 'Vistas']]
    
    for prop in properties:
        # Usar el campo views directamente del modelo Property
        views_count = prop.views
        data.append([prop.title, f"{prop.city}, {prop.state}", views_count])
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Construir el PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
    
    # Add main image to each property
    for prop in properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    context = {
        'properties': properties,
        'query': query,
    }
    
    return render(request, 'real_estate/search_results.html', context)


# Add the discounted_properties function at the module level
def discounted_properties(request):
    """API endpoint to get properties with discounts"""
    properties = Property.objects.filter(discount_percentage__gt=0)
    
    properties_data = []
    for prop in properties:
        discounted_price = float(prop.price) - (float(prop.price) * float(prop.discount_percentage) / 100)
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'price': float(prop.price),
            'discount_percentage': float(prop.discount_percentage),
            'discounted_price': round(discounted_price, 2)
        })
    
    return JsonResponse({'properties': properties_data})


@login_required
def call_tracking_dashboard(request):
    """View to display a list of properties with call statistics"""
    # Get properties owned by the current user
    properties = Property.objects.filter(owner=request.user)
    
    # Get call statistics for each property
    property_stats = []
    for property in properties:
        # In a real implementation, you would have a PropertyCall model
        # For now, we'll create dummy data
        property_stats.append({
            'property': property,
            'total_calls': 0,
            'completed_calls': 0,
            'missed_calls': 0,
            'last_call': None
        })
    
    context = {
        'property_stats': property_stats
    }
    
    return render(request, 'real_estate/call_tracking_list.html', context)


def debug_search(request):
    """A temporary debug view to check if properties exist"""
    query = "Celaya"
    
    ventas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='venta'
    )
    
    rentas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='renta'
    )
    
    data = {
        'query': query,
        'ventas_count': ventas.count(),
        'rentas_count': rentas.count(),
        'ventas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in ventas],
        'rentas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in rentas],
    }
    
    return JsonResponse(data)


@require_POST
def property_contact(request, property_id):
    """Handle property contact form submissions"""
    try:
        property_obj = Property.objects.get(id=property_id)
        
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Create contact record
        contact = PropertyContact.objects.create(
            property=property_obj,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        return JsonResponse({'success': True, 'message': 'Mensaje enviado correctamente'})
    except Property.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Propiedad no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Añadir una vista para mostrar los contactos de las propiedades del usuario
@login_required
def property_contacts(request):
    """View to display contacts for properties owned by the current user"""
    # Get properties owned by the current user
    user_properties = Property.objects.filter(owner=request.user)
    
    # Get contacts for those properties
    contacts = PropertyContact.objects.filter(property__in=user_properties)
    
    context = {
        'contacts': contacts
    }
    
    return render(request, 'real_estate/property_contacts.html', context)


from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json

def estadisticas_vistas(request):
    # Obtener datos para el gráfico mensual
    year = datetime.now().year
    monthly_views = Property.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_views=Sum('views')  # Ahora Sum está definido
    ).order_by('month')

    # Convertir los datos a un formato que pueda ser serializado
    monthly_data = [
        {
            'month': item['month'].strftime('%Y-%m-%d'),
            'total_views': item['total_views'] or 0
        }
        for item in monthly_views
    ]

    # Obtener las propiedades más vistas
    top_properties = Property.objects.order_by('-views')[:10]

    context = {
        'monthly_views': json.dumps(monthly_data, cls=DjangoJSONEncoder),
        'top_properties': top_properties,
    }
    return render(request, 'real_estate/estadisticas.html', context)


# Agregar esta nueva vista para generar el PDF
def estadisticas_pdf(request):
    # Crear un objeto de respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estadisticas_inmobiliaria.pdf"'
    
    # Crear el documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos para el documento
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título del documento
    elements.append(Paragraph("Relación de vistas de propiedades", title_style))
    elements.append(Spacer(1, 20))
    
    # Obtener los datos de propiedades (ajusta esto según tu modelo)
    from .models import Property
    
    # Datos para la tabla
    properties = Property.objects.all()
    data = [['Propiedad', 'Ubicación', 'Vistas']]
    
    for prop in properties:
        # Usar el campo views directamente del modelo Property
        views_count = prop.views
        data.append([prop.title, f"{prop.city}, {prop.state}", views_count])
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Construir el PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
    
    # Add main image to each property
    for prop in properties:
        main_images = prop.images.filter(is_main=True)
        if main_images.exists():
            prop.main_image = main_images.first()
        else:
            prop.main_image = prop.images.first() if prop.images.exists() else None
    
    context = {
        'properties': properties,
        'query': query,
    }
    
    return render(request, 'real_estate/search_results.html', context)


# Add the discounted_properties function at the module level
def discounted_properties(request):
    """API endpoint to get properties with discounts"""
    properties = Property.objects.filter(discount_percentage__gt=0)
    
    properties_data = []
    for prop in properties:
        discounted_price = float(prop.price) - (float(prop.price) * float(prop.discount_percentage) / 100)
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'price': float(prop.price),
            'discount_percentage': float(prop.discount_percentage),
            'discounted_price': round(discounted_price, 2)
        })
    
    return JsonResponse({'properties': properties_data})


@login_required
def call_tracking_dashboard(request):
    """View to display a list of properties with call statistics"""
    # Get properties owned by the current user
    properties = Property.objects.filter(owner=request.user)
    
    # Get call statistics for each property
    property_stats = []
    for property in properties:
        # In a real implementation, you would have a PropertyCall model
        # For now, we'll create dummy data
        property_stats.append({
            'property': property,
            'total_calls': 0,
            'completed_calls': 0,
            'missed_calls': 0,
            'last_call': None
        })
    
    context = {
        'property_stats': property_stats
    }
    
    return render(request, 'real_estate/call_tracking_list.html', context)


def debug_search(request):
    """A temporary debug view to check if properties exist"""
    query = "Celaya"
    
    ventas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='venta'
    )
    
    rentas = Property.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(address__icontains=query) |
        Q(city__icontains=query),
        listing_type='renta'
    )
    
    data = {
        'query': query,
        'ventas_count': ventas.count(),
        'rentas_count': rentas.count(),
        'ventas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in ventas],
        'rentas': [{'id': p.id, 'title': p.title, 'city': p.city} for p in rentas],
    }
    
    return JsonResponse(data)


@require_POST
def property_contact(request, property_id):
    """Handle property contact form submissions"""
    try:
        property_obj = Property.objects.get(id=property_id)
        
        # Get form data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Create contact record
        contact = PropertyContact.objects.create(
            property=property_obj,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        return JsonResponse({'success': True, 'message': 'Mensaje enviado correctamente'})
    except Property.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Propiedad no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Añadir una vista para mostrar los contactos de las propiedades del usuario
@login_required
def property_contacts(request):
    """View to display contacts for properties owned by the current user"""
    # Get properties owned by the current user
    user_properties = Property.objects.filter(owner=request.user)
    
    # Get contacts for those properties
    contacts = PropertyContact.objects.filter(property__in=user_properties)
    
    context = {
        'contacts': contacts
    }
    
    return render(request, 'real_estate/property_contacts.html', context)


from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json

def estadisticas_vistas(request):
    # Obtener datos para el gráfico mensual
    year = datetime.now().year
    monthly_views = Property.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_views=Sum('views')  # Ahora Sum está definido
    ).order_by('month')

    # Convertir los datos a un formato que pueda ser serializado
    monthly_data = [
        {
            'month': item['month'].strftime('%Y-%m-%d'),
            'total_views': item['total_views'] or 0
        }
        for item in monthly_views
    ]

    # Obtener las propiedades más vistas
    top_properties = Property.objects.order_by('-views')[:10]

    context = {
        'monthly_views': json.dumps(monthly_data, cls=DjangoJSONEncoder),
        'top_properties': top_properties,
    }
    return render(request, 'real_estate/estadisticas.html', context)


# Agregar esta nueva vista para generar el PDF
def generate_property_pdf(request, property_id):
    # Obtener la propiedad
    property = get_object_or_404(Property, id=property_id)
    
    # Crear un buffer para recibir los datos del PDF
    buffer = io.BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título
    elements.append(Paragraph(property.title, title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Precio
    price_text = f"${property.price} MXN"
    if property.listing_type == 'renta':
        price_text += "/mes"
    elements.append(Paragraph(f"Precio: {price_text}", subtitle_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Características principales
    elements.append(Paragraph("Características Principales:", subtitle_style))
    
    data = [
        ["Superficie", f"{property.area} m²"],
        ["Recámaras", str(property.bedrooms)],
        ["Baños", str(property.bathrooms)],
    ]
    
    if property.parking_spaces > 0:
        data.append(["Estacionamiento", f"{property.parking_spaces} autos"])
    
    data.append(["Tipo", property.get_property_type_display()])
    
    # Crear tabla
    table = Table(data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Descripción
    elements.append(Paragraph("Descripción:", subtitle_style))
    elements.append(Paragraph(property.description, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Dirección
    elements.append(Paragraph("Ubicación:", subtitle_style))
    elements.append(Paragraph(property.address, normal_style))
    elements.append(Paragraph(f"{property.city}, {property.state}", normal_style))
    
    # Construir el PDF
    doc.build(elements)
    
    # Preparar la respuesta
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'propiedad-{property.id}.pdf')


@login_required
@require_POST
def reset_views(request):
    try:
        # Obtener propiedades del usuario actual
        properties = Property.objects.filter(owner=request.user)
        
        # Reiniciar vistas a 0
        properties.update(views=0)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def toggle_property_visibility(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        if property_id:
            try:
                property = Property.objects.get(id=property_id, owner=request.user)
                property.is_visible = not property.is_visible
                property.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True, 
                        'is_visible': property.is_visible,
                        'message': f'La propiedad ahora está {"visible" if property.is_visible else "oculta"}'
                    })
                else:
                    # Redirección normal para solicitudes no-AJAX
                    return redirect('my_properties')
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': str(e)})
                else:
                    # Redirección normal para solicitudes no-AJAX
                    return redirect('my_properties')
    
    # Redirección por defecto
    return redirect('my_properties')
