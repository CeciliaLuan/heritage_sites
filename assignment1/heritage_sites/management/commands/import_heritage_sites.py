# heritage_sites/management/commands/import_heritage_sites.py
import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from heritage_sites.models import HeritageSite
from django.conf import settings

class Command(BaseCommand):
    help = 'Imports heritage sites from a CSV file.'

    def handle(self, *args, **kwargs):
        # Path to the CSV file
        csv_path = os.path.join(settings.BASE_DIR, 'heritage_sites', 'data', 'whc-sites-2021.csv')

        # Open the CSV file and create the reader object
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Initialize reader here

            for row in reader:
                try:
                    # Convert latitude and longitude to floats
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])
                    print(f"Latitude: {latitude}, Longitude: {longitude}")  # Debug print
                    
                    # Create HeritageSite object with location data
                    HeritageSite.objects.create(
                        name=row['name_en'],
                        description=row['short_description_en'],
                        latitude=latitude,
                        longitude=longitude,
                        location=Point(longitude, latitude)  # Longitude first, then latitude
                    )
                except ValueError as e:
                    print(f"Skipping row due to error: {e}")  # Handle any parsing errors
                except KeyError as e:
                    print(f"Missing key in row: {e}")  # Handle missing columns
