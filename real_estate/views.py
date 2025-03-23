from django.shortcuts import render, get_object_or_404
from .models import Property, PropertyImage
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageForm
from django.forms import modelformset_factory

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
    properties = Property.objects.filter(listing_type='venta')
    
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
            prop.main_image = None
    
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
    
    return render(request, 'real_estate/ventas.html', {
        'properties': properties,
        'cities': cities,
        'filters': filters
    })

def renta(request):
    properties = Property.objects.filter(listing_type='renta')
    
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
            prop.main_image = None
    
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
        'filters': filters
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
            # Redirect all users to admin
            return redirect('/admin/')
        else:
            # Return an error message for invalid login
            return render(request, 'real_estate/login.html', {
                'form_errors': True,
                'error_message': 'Usuario o contraseña incorrectos'
            })
    
    return render(request, 'real_estate/login.html')

def detalle_propiedad(request, id):
    property = get_object_or_404(Property, id=id)
    
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
