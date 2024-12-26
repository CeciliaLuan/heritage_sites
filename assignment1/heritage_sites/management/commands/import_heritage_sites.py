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

        # Open the CSV file and set up a CSV reader
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Process each row in the CSV file
                for row in reader:
                    try:
                        latitude = float(row['latitude'])
                        longitude = float(row['longitude'])
                        print(f"Latitude: {latitude}, Longitude: {longitude}")  # Debug print
                        
                        # Only create if latitude and longitude are valid
                        HeritageSite.objects.create(
                            name=row['name_en'],
                            description=row['short_description_en'],
                            latitude=latitude,
                            longitude=longitude,
                            location=Point(longitude, latitude)  # Longitude first, then latitude
                        )
                    except ValueError as e:
                        print(f"Skipping row due to error: {e}")  # Handle any parsing errors
        except FileNotFoundError:
            print(f"The file {csv_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
