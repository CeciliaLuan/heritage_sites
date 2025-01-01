from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import HeritageSite, Profile, Favourite  # Ensure Favorite is imported
import json
from rest_framework import generics, permissions
from .serializers import HeritageSiteSerializer, FavouriteSerializer


# View that reads the location and passes it to the map
@login_required
def map_view(request):
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
        'username': request.user.username,  # Pass the username here
        'heritage_sites_data': heritage_sites_data
    }
    return render(request, 'heritage_sites.html', context)


# View for updating user's location (via Geolocation API)
@csrf_exempt
@login_required
def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Update the user's profile location
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
            
            return redirect('heritage_sites')  # Redirect to the map page after registration
    else:
        form = UserCreationForm()
    
    # Add form-control class to each form field
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'signup.html', {'form': form})


@csrf_exempt
@login_required
def add_to_favourites(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Log received data for debugging
            print("Received data on server:", data)

            # Validate fields
            required_fields = ['site_name', 'site_description', 'latitude', 'longitude']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)

            # Create a new favourite
            Favourite.objects.create(
                user=request.user,
                site_name=data['site_name'],
                site_description=data['site_description'],
                latitude=data['latitude'],
                longitude=data['longitude']
            )
            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            print("Unexpected error:", e)
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def favourites_view(request):
    """
    Render the My Favorites page.
    Dynamically fetch and display the logged-in user's favorite heritage sites.
    """
    if request.method == "GET":
        # Fetch the user's favorites from the database
        user_favourites = Favourite.objects.filter(user=request.user)

        # Prepare the data for rendering
        favourites_data = [
            {
                "id": favourite.id,
                "site_name": favourite.site_name,
                "site_description": favourite.site_description,
                "latitude": favourite.latitude,
                "longitude": favourite.longitude,
            }
            for favourite in user_favourites
        ]

        # Pass the data to the template
        return render(request, 'favourites.html', {"favourites": favourites_data})

@csrf_exempt
@login_required
def remove_favourite(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        favourite = Favourite.objects.filter(id=data.get('id'), user=request.user).first()
        if favourite:
            favourite.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Favourite not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# ============================================
# DRF API Views
# ============================================

class HeritageSiteListView(generics.ListAPIView):
    """
    API view for listing all heritage sites.
    """
    queryset = HeritageSite.objects.all()
    serializer_class = HeritageSiteSerializer
    permission_classes = [permissions.AllowAny]


class FavouriteListView(generics.ListCreateAPIView):
    """
    API view for listing and creating favourite sites.
    """
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteDetailView(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving or deleting a single favourite site.
    """
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
