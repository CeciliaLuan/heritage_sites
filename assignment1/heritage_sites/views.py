from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.auth import login, logout
from .models import HeritageSite, Profile  # Ensure Profile is imported if it's used
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# View that reads the location and passes it to the map
def map_view(request):
    if request.user.is_authenticated:
        # Get all HeritageSites
        heritage_sites = HeritageSite.objects.all()
        
        # Prepare the data for the map: List of heritage sites with their name and location
        heritage_sites_data = [
            {
                "name": site.name,
                "description": site.description,
                "latitude": site.location.y,  # Using .y for latitude
                "longitude": site.location.x,  # Using .x for longitude
            }
            for site in heritage_sites
        ]
        
        # Context to pass to the template
        context = {
            'user': request.user,
            'heritage_sites_data': heritage_sites_data
        }
        return render(request, 'heritage_sites.html', context)
    else:
        return redirect('login')  # Redirect to login if user is not authenticated


# View for updating user's location (via Geolocation API)
def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Update the user's profile location (if necessary)
        user_profile = request.user.profile  # Assuming the Profile is linked via OneToOneField
        user_profile.location = Point(float(longitude), float(latitude))
        user_profile.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# Login view with form styling
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('heritage_sites')  # Redirect to the map page after login
    else:
        form = AuthenticationForm()
    
    # Add form-control class to each form field
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login after logging out


# Signup view for user registration
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            login(request, user)  # Automatically log the user in after registration
            
            # Create a profile for the user (optional)
            Profile.objects.create(user=user)  # Make sure Profile model exists
            
            return redirect('signup')  # Redirect to the map page after registration
    else:
        form = UserCreationForm()
    
    # Add form-control class to each form field
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'signup.html', {'form': form})
