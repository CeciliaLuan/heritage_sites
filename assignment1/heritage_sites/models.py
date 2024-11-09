from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

# Get the User model (for authentication purposes)
User = get_user_model()

# Profile model for user location
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(null=True, blank=True)  # Stores user's latitude and longitude

    def __str__(self):
        return self.user.username

class HeritageSite(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    # GeoDjango-specific: using PointField to store geographic coordinates (latitude, longitude)
    location = models.PointField(default=Point(0.0, 0.0))

    # Returns the string representation of the model
    def __str__(self):
        return self.name

# Utility function to set or update the user's location
def set_user_location(user_id, latitude, longitude):
    User = get_user_model()  # Get the User model
    user = User.objects.get(id=user_id)

    # Create a Point object from the longitude and latitude
    location = Point(longitude, latitude)  # Point takes (longitude, latitude)

    # Create or update the user's profile
    profile, created = Profile.objects.get_or_create(user=user)

    # Update the location
    profile.location = location
    profile.save()

    return profile
