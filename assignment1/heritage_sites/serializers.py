from rest_framework import serializers
from .models import HeritageSite, Favourite

class HeritageSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageSite
        fields = ['id', 'name', 'description', 'latitude', 'longitude']

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ['id', 'site_name', 'site_description', 'latitude', 'longitude', 'user']
        read_only_fields = ['user']
